import streamlit as st
import boto3
import pandas as pd
import plotly.express as px
from decimal import Decimal
import os , re

# AWS Configuration (using environment variables - BEST PRACTICE)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "ioTDataTimeSeries")

# DynamoDB Resource
try:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE)
except Exception as e:
    st.error(f"Error connecting to DynamoDB: {e}")
    st.stop()

st.title("IoT Data Stream Visualization")

try:
    # Scan DynamoDB table with pagination
    items = []
    response = table.scan()
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    if not items:
        st.warning("No data found in DynamoDB table.")
    else:
        df = pd.DataFrame(items)

        # Convert 'Time' to datetime
        try:
            df['Time'] = pd.to_numeric(df['Time'])
            df['Time'] = pd.to_datetime(df['Time'], unit='s')
        except (TypeError, ValueError) as e:
            st.error(f"Error converting 'Time' to datetime: {e}")
            st.write("DataFrame before Time conversion error:")
            st.write(df)
            st.stop()

        # Convert 'value' to numeric (handling Decimal from DynamoDB)
        try:
            df['value'] = df['value'].apply(lambda x: float(Decimal(str(x))))
        except (TypeError, ValueError, AttributeError) as e:
            st.error(f"Error converting 'value' to numeric: {e}")
            st.write("DataFrame before Value conversion error:")
            st.write(df)
            st.stop()

        # --- Interactive Plot with Filtering and Facets ---
        st.subheader("Interactive Chart")

        # Create filters (using multiselect)
        sensor_types = sorted(df['sensor_type'].unique())
        selected_sensor_types = st.multiselect("Select Sensor Type(s)", sensor_types, default=sensor_types)

        locations = sorted(df['location'].unique())
        selected_locations = st.multiselect("Select Location(s)", locations, default=locations)

        devices = sorted(df['device_id'].unique())
        selected_devices = st.multiselect("Select Device(s)", devices, default=devices)

        # Filter the DataFrame
        filtered_df = df[
            df['sensor_type'].isin(selected_sensor_types) &
            df['location'].isin(selected_locations) &
            df['device_id'].isin(selected_devices)
        ]

        if not filtered_df.empty: 
            filtered_df['location'] = filtered_df['location'].apply(lambda loc: re.sub(r'Warehouse_(\d+)', r'WH_\1', loc))
            fig = px.scatter(filtered_df, x="Time", y="value", color="device_id",
                     facet_col="sensor_type", facet_row="location",
                     title="IoT Sensor Data by Sensor Type and Location")
            fig.update_layout(xaxis_title="Time", yaxis_title="Sensor Value")
            st.plotly_chart(fig)

            st.subheader("Filtered Data")
            st.dataframe(filtered_df)

        else:
            st.warning("No data matches the selected filters.")

except Exception as e:
    st.error(f"A general error occurred: {e}")