import streamlit as st
import boto3
import pandas as pd
import plotly.express as px

# AWS Configuration (Best practice: use IAM roles or environment variables)
AWS_REGION = "us-east-1"  # Replace with your AWS region
DYNAMODB_TABLE = "ioTDataTimeSeries"  # Replace with your DynamoDB table name

# DynamoDB Resource
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

st.title("IoT Data Stream Visualization")

try:
    # Scan DynamoDB table (Limited to 1MB of data; use pagination for larger tables)
    response = table.scan()
    items = response["Items"]

    # Handle pagination for larger datasets (Important!)
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])

    if not items:
        st.warning("No data found in DynamoDB table.")
    else:
        # Convert DynamoDB items to Pandas DataFrame
        df = pd.DataFrame(items)

        # Convert 'Time' to datetime objects
        df['Time'] = pd.to_numeric(df['Time'])
        df['Time'] = pd.to_datetime(df['Time'], unit='s')

        # Convert 'value' to numeric (important for plotting)
        df['value'] = pd.to_numeric(df['value'])

        # Display the DataFrame
        st.subheader("Raw Data")
        st.dataframe(df)

        # Interactive Plotly Express Chart
        st.subheader("Interactive Chart")

        # Create the Plotly Express chart
        # --- Plot ONLY 'value' ---
        st.subheader("Interactive Chart (Value Only)")
        fig = px.scatter(df, x="Time", y="value", title="IoT Sensor Value Over Time") #removed color
        fig.update_layout(xaxis_title="Time", yaxis_title="Sensor Value")
        st.plotly_chart(fig)

        # Add other charts or analysis as needed 
        st.subheader("Data Summary")
        st.write(df.describe())

except Exception as e:
    st.error(f"Error retrieving or processing data: {e}")