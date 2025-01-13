
```markdown
# AWS IoT Projects Overview

This repository showcases several Node.js  & Pyhton projects that demonstrate how to:

1. **Manage device certificates** related to an AWS IoT Core device (stored in the `.certs/` folder).  
2. **Send a single MQTT message** to AWS IoT Core.  
3. **Send multiple MQTT messages** in JSON format:
   ```json
   {
     "device_id": "device_1",
     "sensor_type": "Temperature",
     "location": "Warehouse_2",
     "value": 42.5
   }
   ```
4. **Base64-encode certificates** and store them in AWS Secrets Manager.  
5. **Use certificates** (retrieved from AWS Secrets Manager) to send multiple MQTT messages to AWS IoT Core.

Below is a high-level summary of the projects and how they fit together.

---

## 1. Certificates in `.certs/`

- The folder `.certs/` contains PEM files for your AWS IoT device:
  - **device-private.pem.key**  
  - **device-certificate.pem.crt**  
  - **AmazonRootCA1.pem**  
- These certificates and keys allow secure TLS connections to **AWS IoT Core**.  
- Typically, you configure an IoT Thing in the [AWS IoT Console](https://console.aws.amazon.com/iot/home) and download these credentials into your `.certs/` folder.

---

## 2. Sending a Single Message to AWS IoT Core

One of the examples demonstrates how to send a **single JSON message** via MQTT to an AWS IoT topic. It covers:

1. **Loading** the `.pem` certificates from `.certs/`.  
2. **Using** the [aws-iot-device-sdk](https://www.npmjs.com/package/aws-iot-device-sdk) in Node.js.  
3. **Connecting** to your IoT endpoint (e.g., `xxxxxxxx-ats.iot.us-east-1.amazonaws.com`).  
4. **Publishing** a message (e.g., `{"hello": "iot"}`) to a topic like `my/test/topic`.

---

## 3. Sending Multiple JSON Messages

Another example expands on this by **repeatedly publishing** messages with the following payload structure:

```js
{
  device_id: deviceId,
  sensor_type: sensorType,
  location: `Warehouse_${generateRandom(1, 3)}`,
  value: value
}
```

- **device_id**: A unique device identifier (e.g., `device_3`).  
- **sensor_type**: Fixed per device (e.g., “Pressure” or “Temperature”).  
- **location**: Randomly selected from `Warehouse_1`, `Warehouse_2`, or `Warehouse_3`.  
- **value**: A random reading (e.g., temperature in Celsius or pressure in Bar).

This project uses a **timer** (e.g., an interval every 4 seconds) to publish multiple sensor readings to a topic (e.g., `iot/sub`) on AWS IoT Core.

---

## 4. Base64-Encoding Certificates & Storing in AWS Secrets Manager

We show how to:

1. **Convert** each PEM file (`.key`, `.crt`, `AmazonRootCA1.pem`) into **base64**:
   ```bash
   base64 device-private.pem.key > device-private.txt
   base64 device-certificate.pem.crt > device-certificate.txt
   base64 AmazonRootCA1.pem > AmazonRootCA1.txt
   ```
2. **Create a JSON** file containing all three base64-encoded strings:
   ```json
   {
     "PrivateKey": "<base64-of-device-private-key>",
     "Cert": "<base64-of-device-certificate>",
     "AmazonRootCA": "<base64-of-root-ca>"
   }
   ```
3. **Store** that JSON in AWS Secrets Manager under a secret name like `iot/cert/prod`.

---

## 5. Using Certificates from Secrets Manager to Send Multiple MQTT Messages

Finally, we demonstrate **retrieving** certificates from Secrets Manager and using them **in-memory** (rather than from local files). The steps include:

1. **Calling** `GetSecretValue` via the [AWS SDK for JavaScript v3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/).  
2. **Decoding** the base64 strings to raw PEM content.  
3. **Connecting** to AWS IoT using the in-memory PEM data (e.g., `privateKey`, `clientCert`, `caCert`) rather than file paths.  
4. **Publishing** the same sensor messages to the IoT topic (like `iot/sub`).

By centralizing certificates in Secrets Manager, you can manage **rotation**, **access control**, and **audit logs** more effectively.

---

## Project Structure

```
├─ .certs/
│   ├─ device-private.pem.key
│   ├─ device-certificate.pem.crt
│   └─ AmazonRootCA1.pem
├─ single-message/
│   └─ index.js                 # Example sending a single message
├─ multi-message/
│   └─ index.js                 # Example sending multiple messages w/ random data
├─ secrets-base64/
│   ├─ encode.sh                # Script to base64-encode .pem files
│   └─ push_to_aws.js          # Example storing base64 certs in Secrets Manager
└─ secrets-multi-message/
    └─ index.js                 # Example retrieving from Secrets Manager & publishing
```

> **Note**: The above layout is illustrative. Actual file names and paths may vary.

---

## Prerequisites

- **Node.js** (14+).  
- **AWS CLI** (configured, or AWS credentials set as environment variables).  
- An AWS IoT **Thing**, **certificate**, and **policy** in your AWS account.  
- (Optional) **Secrets Manager** permissions if you’re storing credentials there.

---

## 6. Implementation in GitHub Codespaces

This repository also includes a sample `.devcontainer/devcontainer.json` for working in GitHub Codespaces. It installs:
- **AWS CLI**  
- **Docker in Docker**  
- **Common utilities** (telnet, ping, etc.)  
- **Python, Node.js** if needed

### Steps to Run in Codespaces

1. **Open** this repo in GitHub and click **“Code → Create Codespace on main”** (or your chosen branch).  
2. Wait for the Codespace environment to build. If you see a `.devcontainer` folder, Codespaces will automatically use it to install the required packages and tools.  
3. Once the container is up, open a **terminal** within Codespaces.  
4. Navigate to the relevant project folder (e.g., `multi-message/`).  
5. Install dependencies:
   ```bash
   npm install
   ```
6. **Export** your environment variables, like:
   ```bash
   export AWS_REGION=us-east-1
   export IOT_END_POINT="xxxxxxxx-ats.iot.us-east-1.amazonaws.com"
   ```
7. **Run**:
   ```bash
   node index.js
   ```
   You should see logs indicating successful connection to AWS IoT and repeated published messages.

> **Tip**: If you want to retrieve certificates from Secrets Manager, ensure your IAM role or environment variables allow `secretsmanager:GetSecretValue`. Then run the relevant script (e.g., `secrets-multi-message/index.js`).

---

## Setup & Usage

1. **Clone** this repository or open it in GitHub Codespaces:
   ```bash
   git clone https://github.com/your-account/your-repo.git
   cd your-repo
   ```
2. **Install dependencies** (in each project folder):
   ```bash
   cd single-message
   npm install
   ```
3. **Configure** your AWS Region & IoT endpoint. For example:
   ```bash
   export AWS_REGION=us-east-1
   export IOT_END_POINT="xxxxxxxx-ats.iot.us-east-1.amazonaws.com"
   ```
4. **Run** the single-message example:
   ```bash
   node index.js
   ```
   Or the multi-message example:
   ```bash
   cd ../multi-message
   node index.js
   ```
5. **Base64 encode** your `.pem` files and store them in Secrets Manager (see `secrets-base64/`), then run the script that retrieves them and sends messages (in `secrets-multi-message/`).

---

## Conclusion

This repo illustrates various AWS IoT Core scenarios, from **basic** single-message publishing to **storing certificates** securely in **AWS Secrets Manager** and **sending repeated sensor data**. By leveraging GitHub Codespaces, you can develop and test these IoT features quickly without worrying about local environment setup.  


```