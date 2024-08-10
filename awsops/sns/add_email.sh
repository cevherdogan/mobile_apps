#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 <topic_arn> <email> [AWS_PROFILE]"
    echo "Example: $0 arn:aws:sns:us-east-1:123456789012:MyFirstTopic example@example.com myawsprofile"
    exit 1
}

# Check if help is requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
fi

# Ensure topic ARN and email address are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: Topic ARN and email address are required."
    usage
fi

TOPIC_ARN=$1
EMAIL=$2
PROFILE=${3:-default}

# Validate the AWS profile
if ! aws configure list-profiles | grep -q "^$PROFILE$"; then
    echo "Error: AWS profile '$PROFILE' not found."
    usage
fi

# Subscribe the email address to the SNS topic
aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$EMAIL" --profile "$PROFILE"

echo "Email subscription request sent to $EMAIL for topic $TOPIC_ARN with profile $PROFILE."


