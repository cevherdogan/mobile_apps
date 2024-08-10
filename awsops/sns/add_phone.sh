#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 <topic_arn> <phone_number> [AWS_PROFILE]"
    echo "Example: $0 arn:aws:sns:us-east-1:123456789012:MyFirstTopic +1234567890 myawsprofile"
    exit 1
}

# Check if help is requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
fi

# Ensure topic ARN and phone number are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: Topic ARN and phone number are required."
    usage
fi

TOPIC_ARN=$1
PHONE_NUMBER=$2
PROFILE=${3:-default}

# Validate the AWS profile
if ! aws configure list-profiles | grep -q "^$PROFILE$"; then
    echo "Error: AWS profile '$PROFILE' not found."
    usage
fi

# Subscribe the phone number to the SNS topic
aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sms --notification-endpoint "$PHONE_NUMBER" --profile "$PROFILE"

echo "SMS subscription request sent to $PHONE_NUMBER for topic $TOPIC_ARN with profile $PROFILE."
