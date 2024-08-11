#!/bin/bash

# Function to load and delete topics from a configuration file
cleanup_topics_from_config() {
  local CONFIG_FILE="$1"

  if [ ! -f "$CONFIG_FILE" ]; then
    echo "Configuration file not found: $CONFIG_FILE"
    return
  fi

  AWS_ACCOUNT_ID=$(jq -r '.aws_account_id // empty' "$CONFIG_FILE")
  REGION=$(jq -r '.region // "us-east-1"' "$CONFIG_FILE")  # Default to 'us-east-1' if region is not set
  SNS_TOPIC_PREFIX=$(jq -r '.sns_topic_prefix // ""' "$CONFIG_FILE")
  PROFILE=$(jq -r '.aws_profile // "default"' "$CONFIG_FILE")

  echo "Processing cleanup for topics from $CONFIG_FILE with prefix '$SNS_TOPIC_PREFIX'..."

  # List all SNS topics
  TOPICS=$(aws sns list-topics --region "$REGION" --profile "$PROFILE" --query 'Topics[*].TopicArn' --output text)

  # Loop through each topic and delete if it matches the prefix or is explicitly listed in the config
  for TOPIC_ARN in $TOPICS; do
    TOPIC_NAME=$(echo "$TOPIC_ARN" | awk -F':' '{print $NF}')
    
    # Check if the topic matches the prefix or is explicitly listed
    if [[ "$TOPIC_ARN" == *"$SNS_TOPIC_PREFIX"* ]] || jq -e ".topics | has(\"$TOPIC_NAME\")" "$CONFIG_FILE" > /dev/null; then
      echo "Deleting topic: $TOPIC_ARN"
      aws sns delete-topic --topic-arn "$TOPIC_ARN" --region "$REGION" --profile "$PROFILE"
    fi
  done
}

# Run cleanup for both configuration files
cleanup_topics_from_config "soft_switch/config/sns_config.json"

echo "Cleanup complete."


