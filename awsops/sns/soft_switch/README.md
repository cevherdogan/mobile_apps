# AWS SNS Topic Router

This project provides an API for routing messages to specific AWS SNS topics based on a predefined prefix. The API reads from a configuration file to determine the appropriate topics and handles errors gracefully.

## Prerequisites

- Python 3.8+
- AWS CLI configured with the appropriate profiles
- Required Python packages (see `requirements.txt`)

## Setup

```yaml
flask_app/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── sns_utils.py
├── config.py
├── run.py
├── requirements.txt
└── README.md
```


1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd awsops/sns/soft_switch
    ```

2. **Install dependencies:**

    ```bash
    pip install -r ../../requirements.txt
    ```

3. **Create Configuration:**

    The `soft_switch/config/sns_config.json` file contains sensitive information such as AWS account details, region, and SNS topic ARNs, and it is added to `.gitignore` to avoid committing it to version control.

    Here is an example configuration file structure:

    ```json
    {
        "aws_account_id": "your-aws-account-id",
        "region": "your-aws-region",
        "sns_topic_prefix": "test_routable_",
        "aws_profile": "your-aws-profile",
        "topics": {
            "sns_topic1": {
                "type": "sms",
                "sms_subscribers": ["+your-phone-number"],
                "email_subscribers": []
            },
            "email_topic1": {
                "type": "email",
                "sms_subscribers": [],
                "email_subscribers": ["your-email1@example.com", "your-email2@example.com"]
            },
            "mixed_topic1": {
                "type": "mixed",
                "sms_subscribers": ["+your-phone-number"],
                "email_subscribers": ["your-email3@example.com"]
            }
        }
    }
    ```

    Replace the placeholders (`your-aws-account-id`, `your-aws-region`, `your-aws-profile`, etc.) with your actual details.

    **Important:** Ensure that this file is not shared or committed to version control. It should remain secure.

4. **Run the API:**

    ```bash
    python app.py
    ```

5. **Test the API:**

    Use `curl` or Postman to send requests to the API.

    ```bash
    curl -X POST http://localhost:5000/publish -H "Content-Type: application/json" -d '{
        "type": "sms",
        "message": "This is a test SMS message."
    }'
    ```

## Handling Sensitive Information

- **Masking Secrets:** Ensure that any sensitive information such as AWS account details, profile names, and ARNs are not included in the version control system. Use `.gitignore` to exclude files like `sns_config.json` that contain such details.
  
- **Environment Variables:** Consider using environment variables or secret management tools like AWS Secrets Manager to manage sensitive data securely.
  
- **Configuration Management:** If deploying in a production environment, make sure to use secure methods to inject configuration values, such as using environment variables or encrypted configuration files.

## Error Handling

- The API will return a `400 Bad Request` if the message type or body is invalid.
- If the configuration file is missing or incorrect, the API will return a `500 Internal Server Error` with details.
- The API also handles AWS profile and region configuration errors.

## License

This project is licensed under the MIT License.


