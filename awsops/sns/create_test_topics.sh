#!/bin/bash

# Load configuration from sns_config.json
CONFIG_FILE="soft_switch/config/sns_config.json"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Configuration file not found: $CONFIG_FILE"
  exit 1
fi

AWS_ACCOUNT_ID=$(jq -r '.aws_account_id' "$CONFIG_FILE")
REGION=$(jq -r '.region' "$CONFIG_FILE")
SNS_TOPIC_PREFIX=$(jq -r '.sns_topic_prefix' "$CONFIG_FILE")
PROFILE=$(jq -r '.aws_profile' "$CONFIG_FILE")

echo "Starting topic creation based on configuration in $CONFIG_FILE..."

# Iterate through the topics in the configuration
TOPICS=$(jq -r '.topics | keys[]' "$CONFIG_FILE")

for TOPIC in $TOPICS; do
  FULL_TOPIC_NAME="${SNS_TOPIC_PREFIX}${TOPIC}"

  # Check if the topic already exists
  EXISTING_TOPIC_ARN=$(aws sns list-topics --region "$REGION" --profile "$PROFILE" --query "Topics[?ends_with(TopicArn, ':${FULL_TOPIC_NAME}')].TopicArn" --output text)

  if [ -z "$EXISTING_TOPIC_ARN" ]; then
    # Create the topic if it doesn't exist
    echo "[INFO] Creating topic '$FULL_TOPIC_NAME'..."
    TOPIC_ARN=$(aws sns create-topic --name "$FULL_TOPIC_NAME" --region "$REGION" --profile "$PROFILE" --query "TopicArn" --output text)
    echo "[INFO] Topic created successfully: $TOPIC_ARN"
  else
    TOPIC_ARN=$EXISTING_TOPIC_ARN
    echo "[WARNING] Topic already exists: $TOPIC_ARN"
  fi

  # Add SMS subscriptions
  SMS_SUBSCRIBERS=$(jq -r ".topics[\"$TOPIC\"].sms_subscribers[]" "$CONFIG_FILE")
  for SMS in $SMS_SUBSCRIBERS; do
    if [ -n "$SMS" ]; then
      echo "[INFO] Adding SMS subscription for $SMS to topic '$FULL_TOPIC_NAME'..."
      aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sms --notification-endpoint "$SMS" --region "$REGION" --profile "$PROFILE"
    fi
  done

  # Add Email subscriptions
  EMAIL_SUBSCRIBERS=$(jq -r ".topics[\"$TOPIC\"].email_subscribers[]" "$CONFIG_FILE")
  for EMAIL in $EMAIL_SUBSCRIBERS; do
    if [ -n "$EMAIL" ]; then
      echo "[INFO] Adding email subscription for $EMAIL to topic '$FULL_TOPIC_NAME'..."
      aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$EMAIL" --region "$REGION" --profile "$PROFILE"
    fi
  done
done

echo "Topic creation and subscription process completed."


