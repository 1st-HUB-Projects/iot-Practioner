Markdown
# AWS IoT Core Device Simulator

This project simulates an IoT device that connects to AWS IoT Core and publishes random sensor data (temperature and pressure) to the `iot/sub` topic every 2 seconds.

## Overview

The script uses the `aws-iot-device-sdk` for Node.js to establish a secure MQTT connection with AWS IoT Core. It then generates simulated sensor data and publishes it in JSON format.

## Prerequisites

1.  **AWS Account:** You need an active AWS account.
2.  **AWS IoT Core Setup:**
    *   Create a **Thing** in AWS IoT Core.
    *   Generate a **certificate** and **private key** for your Thing.
    *   Download the **Amazon Root CA 1** certificate.
    *   Create a **policy** that allows your Thing to connect, publish, subscribe, and receive (adjust permissions as needed).
    *   Attach the policy to the certificate, and attach the certificate to the Thing.
3.  **Node.js and npm:** Make sure you have Node.js and npm installed on your system or in your AWS Codespaces environment. You can check by running:

    ```bash
    node -v
    npm -v
    ```
4.  **AWS CLI:** Install and configure the AWS CLI. This is optional for running the script but helpful for managing AWS resources.
5.  **Install the AWS IoT Device SDK:**

    ```bash
    npm install aws-iot-device-sdk
    ```

## Project Structure

Iot-Practitioner/
├── .certs/
│   ├── iOTest_PrivateKey.pem    # Your device's private key
│   ├── iOTest_Cert.pem         # Your device's certificate
│   └── AmazonRootCA.pem     # The Amazon Root CA 1 certificate
├── virtualiOT_js/
└── singleMqttMsg.js         # NodeJs program that sends an Mqtt Message to aws IoT Core


*   **`.certs/`:** This directory stores your device's private key, certificate, and the Amazon Root CA certificate. **Important:** Keep this directory secure and do not commit your private key to version control (add `.certs/` to your `.gitignore` file). The leading dot in the folder name makes it a hidden folder; you can make it appear by pressing CTRL + H.
*   **`Check File Permissions`:** This is the main Node.js script that simulates the IoT device.
ls -l: Use ls -l to examine the file permissions of your private key, certificate, and CA certificate within the Codespaces environment:

 ```bash
ls -l ../.certs
```
* Permissions:

iOTest_PrivateKey.pem: Should have read and write permissions for the owner (e.g., -rw------- or -rw-r--r--).
iOTest_Cert.pem: Should have at least read permissions for the owner (e.g., -r--r--r-- or -rw-r--r--).
AmazonRootCA.pem: Should have at least read permissions for the owner.
chmod (if needed):

```bash
chmod 600 ../.certs/iOTest_PrivateKey.pem  # Secure the private key
chmod 644 ../.certs/iOTest_Cert.pem
chmod 644 ../.certs/AmazonRootCA.pem
```
*   **`virtualiOT_js/singleMQTTMsg.js`:** This is the main Node.js script that simulates the IoT device.

## Configuration

1.  **Certificates:**
    *   Place your downloaded private key (`iOTest_PrivateKey.pem`), certificate (`iOTest_Cert.pem`), and the Amazon Root CA 1 certificate (`AmazonRootCA.pem`) into the `.certs/` directory.
2.  **Environment Variables:**
    * This project uses environment variables to manage sensitive information like your AWS IoT endpoint and region. This is a security best practice to avoid hardcoding these values directly in your code.

    * **`IOT_END_POINT`:**  Your AWS IoT Core endpoint. You can find this in the AWS IoT Core console under Settings.
    * **`AWS_DEFAULT_REGION`:** The AWS region where your IoT Core resources are located (e.g., `us-east-1`).

    ### Setting Environment Variables

    The method for setting environment variables depends on your operating system and whether you want to set them temporarily (for the current session) or permanently.

    #### **Linux/macOS**

    **1. Temporary (Current Terminal Session):**

    ```bash
    export IOT_END_POINT="your_iot_endpoint"
    export AWS_DEFAULT_REGION="your_aws_region"
    ```

    *   Replace `your_iot_endpoint` with your actual IoT endpoint and `your_aws_region` with your AWS region.

    **2. Permanent (System-wide):**

    *   **Edit your shell's configuration file:**
        *   **Bash:**  Edit `~/.bashrc`, `~/.bash_profile`, or `~/.profile`.
        *   **Zsh:** Edit `~/.zshrc`.
    *   **Add the following lines:**

    ```bash
    export IOT_END_POINT="your_iot_endpoint"
    export AWS_DEFAULT_REGION="your_aws_region"
    ```

    *   **Save the file and then either:**
        *   Source the configuration file: `source ~/.bashrc` (or the appropriate file for your shell)
        *   Or, open a new terminal window for the changes to take effect.

    #### **Windows**

    **1. Temporary (Current Command Prompt):**

    ```batch
    set IOT_END_POINT=your_iot_endpoint
    set AWS_DEFAULT_REGION=your_aws_region
    ```

    **2. Permanent (System-wide):**

    *   **Through System Properties:**
        1.  Search for "environment variables" in the Windows search bar.
        2.  Select "Edit the system environment variables."
        3.  Click the "Environment Variables..." button.
        4.  Under "System variables," click "New...".
        5.  Enter `IOT_END_POINT` for the "Variable name" and your IoT endpoint for the "Variable value".
        6.  Repeat steps 4-5 for `AWS_DEFAULT_REGION`.
        7.  Click "OK" on all open windows to save the changes.
    *   **Through PowerShell:**

    ```powershell
    [System.Environment]::SetEnvironmentVariable('IOT_END_POINT', 'your_iot_endpoint', 'Machine')
    [System.Environment]::SetEnvironmentVariable('AWS_DEFAULT_REGION', 'your_aws_region', 'Machine')
    ```

    #### **AWS Codespaces**

    *   **Through the .devcontainer.json file:** The recommended method for Codespaces is to define the environment variables within the `.devcontainer/devcontainer.json` file.

        ```json
        {
            // ... other devcontainer.json settings

            "remoteEnv": {
                "IOT_END_POINT": "your_iot_endpoint",
                "AWS_DEFAULT_REGION": "your_aws_region"
            }
        }
        ```

    *  **Through the Codespaces Secrets (Recommended for sensitive values like IOT_END_POINT):**

        1.  In your repository or organization settings on GitHub, go to "Codespaces" -> "Secrets".
        2.  Add a new secret named `IOT_END_POINT` with your endpoint as the value.
        3.  Add another secret named `AWS_DEFAULT_REGION` with your region as the value.
        4.  In your `.devcontainer/devcontainer.json`, add a reference to the secrets:

            ```json
            {
                // ... other devcontainer.json settings

                "remoteEnv": {
                    "IOT_END_POINT": "${localEnv:IOT_END_POINT}",
                    "AWS_DEFAULT_REGION": "${localEnv:AWS_DEFAULT_REGION}"
                }
            }
            ```

        5.  Rebuild your Codespaces container for the changes to take effect.

    #### **Verifying Environment Variables**

    After setting the environment variables, you can verify them by using the following commands or code:

    *   **Linux/macOS:**

        ```bash
        echo $IOT_END_POINT
        echo $AWS_DEFAULT_REGION
        ```

    *   **Windows (Command Prompt):**

        ```batch
        echo %IOT_END_POINT%
        echo %AWS_DEFAULT_REGION%
        ```

    *   **Windows (PowerShell):**

        ```powershell
        $env:IOT_END_POINT
        $env:AWS_DEFAULT_REGION
        ```
    *   **Node.js:**

        ```javascript
        console.log(process.env.IOT_END_POINT);
        console.log(process.env.AWS_DEFAULT_REGION);
        ```

3.  **Update `singleMQTTMsg.js`:**
    *   **`clientId`:** Make sure `"iOTestID"` is unique or matches your Thing name in AWS IoT Core.

## Running the Simulator

1.  Navigate to the project directory in your terminal:

    ```bash
    cd Iot-Practitioner/virtualiOT_js/
    ```

2.  Run the script:

    ```bash
    node singleMQTTMsg.js
    ```

## Output

You should see output similar to this in your console:

Connected to AWS IoT Core
Message sent: {"temperature":"25.43","pressure":"987.65","device_id":"device_3"}
Message sent: {"temperature":"22.12","pressure":"1012.55","device_id":"device_1"}
Message sent: {"temperature":"28.90","pressure":"945.21","device_id":"device_5"}
...


You can also monitor the messages in the AWS IoT Core console:

1.  Go to the AWS IoT Core console.
2.  Click on **"MQTT test client"**.
3.  Subscribe to the topic `iot/sub`.

## Important Security Notes

*   **Never commit your private key to a public repository.** Add the `.certs/` directory to your `.gitignore` file.
*   **Restrict Permissions:** Follow the principle of least privilege when creating your AWS IoT Core policy. Grant only the necessary permissions to your Thing.
*   **Certificate Security:** Store your certificates securely and limit access to them. Consider using a secrets management service like AWS Secrets Manager for production environments.

## Troubleshooting

*   **`Error: Invalid "keyPath" option supplied.`:** This usually means the path to your private key file is incorrect or the file doesn't exist. Double-check the path and file name in `singleMQTTMsg.js`. Also, ensure that you are using the `key` option (not `keyPath`) when passing the certificate content directly as a Buffer or string.
*   **`Error: Invalid "certPath" option supplied.`:** Similar to the above, but for the certificate file. Make sure you are using the `cert` option (not `certPath`).
*   **`Error: Invalid "caPath" option supplied.`:**  Make sure you are using the correct **Amazon Root CA 1** certificate, and the path is correct or you are passing the content directly with the `ca` option.
*   **`Error: Connect error: Not authorized`:** This indicates that the policy attached to your Thing's certificate does not allow the necessary actions (e.g., `iot:Connect`, `iot:Publish`). Review your policy in AWS IoT Core.
*   **No output:** If you don't see any output, check the following:
    *   Is your device successfully connecting to AWS IoT Core? Look for the "Connected to AWS IoT Core" message.
    *   Is your device publishing to the correct topic (`iot/sub`)?
    *   Are you subscribed to the correct topic in the MQTT test client?

## Further Development

*   **Retrieve Certificates from Secrets Manager:** Modify the script to retrieve certificates from AWS Secrets Manager for enhanced security.
*   **Multiple Devices:** Simulate multiple devices with different IDs and sensor types.
*   **More Realistic Data:** Generate more realistic sensor data patterns instead of purely random values.
*   **Error Handling:** Implement more robust error handling and logging.
*   **Command Line Arguments:** Use command-line arguments or environment variables to configure the script instead of hardcoding values.

This README provides a comprehensive guide to understanding, configuring, and running the provided IoT device simulator script. Remember to prioritize security best practices when working with AWS IoT Core and certificates.