#!/bin/bash

# Function to parse YAML using awk
parse_yaml() {
    local prefix=$2
    local s='[[:space:]]*'
    local w='[a-zA-Z0-9_.-]*'
    local fs
    fs="$(echo @|tr @ '\034')"
    sed -ne "s|^\($s\):|\1|" \
         -e "s|^\($s\)\($w\)$s:$s\"\(.*\)\"$s\$|\1$fs\2$fs\3|p" \
         -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  "$1" |
    awk -F"$fs" '{
       indent = length($1)/2;
       vname[indent] = $2;
       for (i in vname) {if (i > indent) {delete vname[i]}}
       if (length($3) > 0) {
          vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
          printf("%s%s%s=\"%s\"\n", "'$prefix'", vn, $2, $3);
       }
    }'
}

# Load configuration from YAML
CONFIG_FILE="restore_config.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Configuration file not found: $CONFIG_FILE"
  exit 1
fi

eval $(parse_yaml "$CONFIG_FILE" "config_")

# Validate required configuration
if [ -z "$config_region" ] || [ -z "$config_aws_account_id" ]; then
  echo "Required configuration missing in $CONFIG_FILE."
  exit 1
fi

echo "Restoring SNS topics in region '$config_region' for AWS account '$config_aws_account_id'..."

# Function to restore a topic and add subscriptions
restore_topic() {
  local topic_name=$1
  local region=$2
  local profile=$3

  echo "Creating topic: $topic_name"
  aws sns create-topic --name "$topic_name" --region "$region" --profile "$profile"

  local email_var="config_topics_${topic_name}_email_subscribers"
  local sms_var="config_topics_${topic_name}_sms_subscribers"

  # Add email subscriptions
  if [ -n "${!email_var}" ]; then
    for email in ${!email_var}; do
      echo "Adding email subscription: $email"
      aws sns subscribe --topic-arn "arn:aws:sns:$region:$config_aws_account_id:$topic_name" \
        --protocol email --notification-endpoint "$email" --region "$region" --profile "$profile"
    done
  fi

  # Add SMS subscriptions
  if [ -n "${!sms_var}" ]; then
    for phone in ${!sms_var}; do
      echo "Adding SMS subscription: $phone"
      aws sns subscribe --topic-arn "arn:aws:sns:$region:$config_aws_account_id:$topic_name" \
        --protocol sms --notification-endpoint "$phone" --region "$region" --profile "$profile"
    done
  fi
}

# Restore topics listed in the YAML configuration
for topic in ${config_topics[@]}; do
  restore_topic "$topic" "$config_region" "$config_aws_profile"
done

echo "Restore complete."

