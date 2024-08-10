#!/bin/bash

# Usage function to display help
usage() {
    echo "Usage: $0 <topic_name> [AWS_PROFILE]"
    echo "Example: $0 MyFirstTopic myawsprofile"
    exit 1
}

# Check if help is requested
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    usage
fi

# Ensure topic name is provided
if [ -z "$1" ]; then
    echo "Error: Topic name is required."
    usage
fi

TOPIC_NAME=$1
PROFILE=${2:-default}

# Validate the AWS profile
if ! aws configure list-profiles | grep -q "^$PROFILE$"; then
    echo "Error: AWS profile '$PROFILE' not found."
    usage
fi

# Create the SNS topic
response=$(aws sns create-topic --name "$TOPIC_NAME" --profile "$PROFILE" 2>&1)

# Check if the topic creation was successful
if [[ "$response" == *"arn:aws:sns"* ]]; then
    topic_arn=$(echo $response | jq -r '.TopicArn')
    echo "Topic created: $topic_arn with profile $PROFILE"
else
    echo "Error creating topic: $response"
    exit 1
fi

