#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 [AWS_PROFILE]"
    echo "Example: $0 myawsprofile"
    exit 1
}

# Check if help is requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
fi

# Check if profile name is provided, else use default
PROFILE=${1:-default}

# Validate the AWS profile
if ! aws configure list-profiles | grep -q "^$PROFILE$"; then
    echo "Error: AWS profile '$PROFILE' not found."
    usage
fi

# List SNS topics using the specified profile
aws sns list-topics --profile "$PROFILE" --query 'Topics[*].TopicArn' --output text


