#!/bin/bash

# Usage: ./add_topic.sh <topic_name> [profile_name]

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <topic_name> [profile_name]"
    exit 1
fi

TOPIC_NAME=$1
PROFILE=${2:-default}  # Eğer profil belirtilmezse, 'default' profili kullanılır.

# Check if the provided profile exists
if ! aws configure list-profiles | grep -q "^$PROFILE$"; then
    echo "Error: The config profile '$PROFILE' could not be found."
    exit 1
fi

# Attempt to create the topic
response=$(aws sns create-topic --name "$TOPIC_NAME" --profile "$PROFILE" 2>&1)

# Check if the topic creation was successful
if [[ "$response" == *"arn:aws:sns"* ]]; then
    topic_arn=$(echo $response | jq -r '.TopicArn')
    echo "Topic created: $topic_arn with profile $PROFILE"
else
    echo "Error creating topic: $response"
    exit 1
fi


