# Managing and Verifying IoT Certificates with Base64 Encoding and AWS Secrets Manager

This README provides a comprehensive guide to encoding, storing, retrieving, and using your IoT certificates securely with AWS Secrets Manager and Codespaces. Remember to follow security best practices and never commit sensitive information like private keys to your Git repository.
Using Base64 start by encoding PEM certificate files , storing them in AWS Secrets Manager, and verifying them using a Python script. 

## 1. Encoding PEM Files with Base64

Before storing your IoT certificate files (private key, device certificate, and CA certificate) in AWS Secrets Manager, you need to encode them into Base64 format. This is because Secrets Manager stores data as strings, and Base64 provides a way to represent binary data (like certificates) in a text-based format.

**Command:**

You can use the `base64` command on Linux, macOS, or Git Bash on Windows to encode each file. The `-w 0` option ensures the output is a single line (no line wrapping):

```bash
base64 -w 0 Private_cert.pem   # Encode your private key
base64 -w 0 iOT_Cert.pem      # Encode your device certificate
base64 -w 0 AmazonRootCA.pem  # Encode the Amazon Root CA certificate
Example:

If your private key file is named iOTest_PrivateKey.pem, the command would be:

Bash
base64 -w 0 iOTest_PrivateKey.pem
This will output the Base64 encoded string to the console. Copy this output for the next step.

Important:

No Line Breaks: Make sure the output is a single, continuous line of text. Some systems might introduce line breaks by default. The -w 0 option in the base64 command (on Linux/macOS) prevents this.
Copy Carefully: When copying and pasting the encoded string, ensure you don't introduce any extra spaces or characters.
2. Storing Encoded Certificates in AWS Secrets Manager
Navigate to Secrets Manager: Go to the AWS Secrets Manager console.

Create a New Secret: Click "Store a new secret".

Secret Type: Choose "Other type of secret".

Plaintext: Select the "Plaintext" tab.

Format as JSON: Paste the Base64 encoded strings into the "Plaintext" box, formatted as a JSON object:

JSON
{
    "PrivateKey": "<Base64 encoded private key>",
    "Cert": "<Base64 encoded certificate>",
    "AmazonRootCA": "<Base64 encoded CA certificate>"
}
 Replace the placeholders with the actual Base64 encoded strings you copied in the previous step.

Secret Name: Give your secret a descriptive name (e.g., iot/device/certificates).

Complete the Process: Follow the remaining steps to create the secret.

3. Verifying Secrets with check_SecretsVal.py
The check_SecretsVal.py Python script helps you retrieve and display the stored secrets from AWS Secrets Manager.

Prerequisites:

boto3 library: You need to install the AWS SDK for Python (Boto3). The requirements.txt file in your project should include boto3. Install it using:

Bash
pip install -r requirements.txt
 Running the Script:

Bash
python check_SecretsVal.py
What the Script Does:

The script will:

Connect to AWS Secrets Manager using your configured AWS credentials (make sure your Codespaces environment has appropriate IAM permissions).
Retrieve the secret you specified (e.g., iot/device/certificates).
Decode the Base64 encoded values back into their original PEM format.
Print the decoded PEM data to the console.
Purpose of Verification:

This script helps you verify that:

The certificates were correctly encoded and stored in Secrets Manager.
You can successfully retrieve and decode them.
The decoded certificates match your original .pem files.
4. Environment Variables in Codespaces
This project relies on environment variables to configure the connection to AWS IoT Core:

AWS_DEFAULT_REGION: Specifies the AWS region where your IoT resources are located (e.g., us-east-1).
IOT_END_POINT: Your AWS IoT Core endpoint. This is specific to your account and region.
Checking Environment Variables:

You can check the current environment variables in your Codespaces terminal using:

Bash
env | grep AWS_
This will display all environment variables that contain "AWS_".

Setting Environment Variables (if needed):

Refer to the documentation on "Setting Environment Variables for AWS IoT Endpoint and Region" in this repository for detailed instructions on setting these variables in different operating systems and in Codespaces. It's recommended to set IOT_END_POINT as a Codespaces secret for better security.

5. Using Certificates in Your IoT Application
When using the aws-iot-device-sdk in your Node.js code to connect to AWS IoT Core:

In-Memory PEM Data: If you have retrieved the decoded PEM data from Secrets Manager (e.g., stored in variables like privateKeyDecoded, certDecoded, caDecoded), use the key, cert, and ca options to pass the data directly:

JavaScript
const device = iot.device({
  key: privateKeyDecoded, // Buffer or string containing the PEM data
  cert: certDecoded,      // Buffer or string containing the PEM data
  ca: caDecoded,         // Buffer or string containing the PEM data
  // ... other options
});
 File Paths: If you have the actual .pem files on disk, use the keyPath, certPath, and caPath options:

JavaScript
const device = iot.device({
  keyPath: './.certs/iOTest_PrivateKey.pem',
  certPath: './.certs/iOTest_Cert.pem',
  caPath: './.certs/AmazonRootCA.pem',
  // ... other options
});
 Important: Do not mix these up. Use either the in-memory options (key, cert, ca) OR the file path options (keyPath, certPath, caPath), not both.

