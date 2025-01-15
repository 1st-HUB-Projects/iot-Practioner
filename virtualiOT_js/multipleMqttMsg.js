const awsIot = require('aws-iot-device-sdk');
const AWS_DEFAULT_REGION = process.env.AWS_DEFAULT_REGION || 'us-east-1';
const IOT_END_POINT = process.env.IOT_END_POINT || 'xxxxxxxxx-ats.iot.us-east-1.amazonaws.com';
const device = awsIot.device({
    keyPath: '../.certs/iOTest_PrivateKey.pem',        // Path to your private key
    certPath: '../.certs/iOTest_Cert.pem',             // Path to your certificate
    caPath: '../.certs/AmazonRootCA.pem',        // Path to AWS Root CA
    clientId: 'iOTestID',            // Device client ID
    host: `${IOT_END_POINT}`  // .iot.${region}.amazonaws.com`   AWS IoT endpoint
});
// Store a mapping between device_id and sensor_type
const deviceSensorMap = {};


function generateRandom(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

// Function to generate the sensor value based on the sensor type
function generateSensorValue(sensorType) {
    let value;
    if (sensorType === "Temperature") {
        value = Math.random() * 110 - 10;
    } else {
        value = Math.random() * 100 + 1;
    }
    return parseFloat(value.toFixed(2)); // Convert to float after toFixed
}

device.on('connect', () => {
    console.log('Device connected to AWS IoT Core');

    // Send data every 2 seconds
    setInterval(() => {
        const deviceId = `device_${generateRandom(1, 5)}`; // Random device ID from 1 to 5

        // Ensure each device has a fixed sensor_type (either "Pressure" or "Temperature")
        if (!deviceSensorMap[deviceId]) {
            deviceSensorMap[deviceId] = (Math.random() < 0.5 ? "Pressure" : "Temperature");
        }

        const sensorType = deviceSensorMap[deviceId];
        const value = generateSensorValue(sensorType); // Generate value based on sensor type

        const payload = JSON.stringify({
            "device_id": deviceId,
            "sensor_type": sensorType,  // Fixed sensor_type based on device_id
            "location": `Warehouse_${generateRandom(1, 3)}`, // Random location: Warehouse_1 to Warehouse_3
            "value": value // Random value based on sensor type
        });

        // Publish to the topic 'iot/sub' every 5"
        device.publish('iot/sub', payload);
        console.log('Message sent:', payload);
    }, 5000);
});


device.on('error', function(error) {
    console.error('Error:', error);
});