#!/bin/bash

# Usage: ./delete_topic.sh <topic_arn> [profile_name]

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <topic_arn> [profile_name]"
    exit 1
fi

TOPIC_ARN=$1
PROFILE=${2:-default}  # Eğer profil belirtilmezse, 'default' profili kullanılır.

aws sns delete-topic --topic-arn "$TOPIC_ARN" --profile "$PROFILE"

echo "Topic deleted: $TOPIC_ARN with profile $PROFILE"


