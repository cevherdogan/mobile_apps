# Simple SNS Test Validation Script

This script, `simple_test_validation.sh`, is designed to automate the validation and testing of your AWS SNS topics and subscriptions. It allows you to list topics, check for pending confirmations, add new subscriptions, and send test messages to both email and SMS subscribers.

## Prerequisites

- **AWS CLI**: Ensure that the AWS CLI is installed and configured with the appropriate profile.
- **Bash**: This script is designed to run in a Bash environment.

## Usage

1. **Make the Script Executable**:

    Before running the script, ensure it is executable:

    ```bash
    chmod +x simple_test_validation.sh
    ```

2. **Run the Script**:

    Execute the script:

    ```bash
    ./simple_test_validation.sh
    ```

3. **Follow the Prompts**:

    The script will guide you through the following steps:

    - **List Topics**: Displays all SNS topics in your account.
    - **Select a Topic**: Prompts you to enter the ARN of the SNS topic you wish to validate.
    - **List Subscriptions**: Lists all subscriptions associated with the selected topic.
    - **Add Subscriptions**: Optionally add a new email or SMS subscription to the selected topic.
    - **Check for Pending Confirmations**: Identifies any subscriptions that are pending confirmation and prompts you for further action.
    - **Send Test Messages**: Allows you to send test email and SMS messages to the selected topic or phone number.

## Example

### Example Execution

```bash
$ ./simple_test_validation.sh
[INFO] Starting simple test validation...
Available SNS Topics:
arn:aws:sns:us-east-1:************:MyFirstTopic	arn:aws:sns:us-east-1:************:user	arn:aws:sns:us-east-1:************:cloudruple-wp-dev-notification-topic	arn:aws:sns:us-east-1:************:cpptopic	arn:aws:sns:us-east-1:************:email_topic1	arn:aws:sns:us-east-1:************:test_routable_email_topic1	arn:aws:sns:us-east-1:************:test_routable_sns_topic1
Enter the ARN of the topic to validate: arn:aws:sns:us-east-1:************:test_routable_email_topic1
[INFO] Listing subscriptions for topic 'arn:aws:sns:us-east-1:************:test_routable_email_topic1'...
Do you want to add an email subscription? (y/n): y
Enter the email to subscribe: masked_email@example.com
[INFO] Adding email subscription for masked_email@example.com to topic 'arn:aws:sns:us-east-1:************:test_routable_email_topic1'...
{
    "SubscriptionArn": "pending confirmation"
}
Do you want to add an SMS subscription? (y/n): y
Enter the phone number to subscribe (e.g., +1234567890): +1234567890
[INFO] Adding SMS subscription for +1234567890 to topic 'arn:aws:sns:us-east-1:************:test_routable_email_topic1'...
{
    "SubscriptionArn": "arn:aws:sns:us-east-1:************:test_routable_email_topic1:c1f5fa3e-fcc1-4662-8bc9-942f91cb09b4"
}
[INFO] Checking for pending confirmations for topic 'arn:aws:sns:us-east-1:************:test_routable_email_topic1'...
[WARNING] Pending confirmations detected for the following subscriptions:
email	masked_email@example.com
Do you want to resend confirmation emails? (y/n): n
[INFO] Skipping confirmation for pending subscriptions.
Do you want to send a test email to this topic? (y/n): y
[INFO] Publishing test email message to topic 'arn:aws:sns:us-east-1:************:test_routable_email_topic1'...
{
    "MessageId": "bbe9241e-9a1d-5495-a38c-7b2f15136535"
}
Do you want to send a test SMS? (y/n): y
Enter the phone number to send the SMS to (e.g., +1234567890): +1234567890
[INFO] Publishing test SMS message to phone number '+1234567890'...
{
    "MessageId": "54c03485-75fc-5f1e-8030-6bb4fae404d7"
}
[INFO] Simple test validation completed.
```

# Masked Values

- ARNs: The account ID has been replaced with ************.
- Emails: The actual email has been replaced with masked_email@example.com.
- Phone Numbers: The actual phone number has been replaced with +1234567890.



