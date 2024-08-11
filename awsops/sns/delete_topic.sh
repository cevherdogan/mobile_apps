#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 <topic_arn> [AWS_PROFILE]"
    echo "Example: $0 arn:aws:sns:us-east-1:123456789012:MyFirstTopic myawsprofile"
    exit 1
}

# Check if help is requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
fi

# Ensure topic ARN is provided
if [ -z "$1" ]; then
    echo "Error: Topic ARN is required."
    usage
fi

TOPIC_ARN=$1
PROFILE=${2:-default}

# Validate the AWS profile
if ! aws configure list-profiles | grep -q "^$PROFILE$"; then
    echo "Error: AWS profile '$PROFILE' not found."
    usage
fi

# Delete the SNS topic
aws sns delete-topic --topic-arn "$TOPIC_ARN" --profile "$PROFILE"

echo "Topic deleted: $TOPIC_ARN with profile $PROFILE"

