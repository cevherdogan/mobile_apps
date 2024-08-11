#!/bin/bash
set -e

# Set the default AWS profile
export AWS_DEFAULT_PROFILE=cevherdogan

CONFIG_FILE="soft_switch/config/sns_config.json"
TOPIC_ARN_FILE="topic_arns.txt"
LOG_FILE="sns_integration.log"

# Function to log messages with timestamps
function log() {
    local LEVEL=$1
    shift
    local MESSAGE=$@
    local TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE" | tee -a "$LOG_FILE"
}

# Function to check if the profile exists
function check_profile() {
    log "INFO" "Checking if AWS profile '$AWS_DEFAULT_PROFILE' exists..."
    if ! aws configure list-profiles | grep -q "^$AWS_DEFAULT_PROFILE$"; then
        log "ERROR" "The config profile '$AWS_DEFAULT_PROFILE' could not be found."
        exit 1
    fi
    log "INFO" "AWS profile '$AWS_DEFAULT_PROFILE' found."
}

# Function to read the configuration file
function read_config() {
    log "INFO" "Reading configuration from $CONFIG_FILE..."
    if [ ! -f "$CONFIG_FILE" ]; then
        log "ERROR" "Configuration file $CONFIG_FILE not found."
        exit 1
    fi
    CONFIG=$(cat "$CONFIG_FILE")

    # Ensure topics exist in the configuration
    if ! echo "$CONFIG" | jq -e '.topics' > /dev/null; then
        log "ERROR" "'topics' key is missing or empty in the configuration file."
        exit 1
    fi
    log "INFO" "Configuration file $CONFIG_FILE read successfully."
}

# Function to add a topic and capture the ARN only if it doesn't already exist
function add_topic() {
    TOPIC_NAME=$1
    FULL_TOPIC_NAME="${sns_topic_prefix}${TOPIC_NAME}"

    log "INFO" "Checking if topic '$FULL_TOPIC_NAME' already exists..."
    # Check if the topic already exists
    existing_arn=$(aws sns list-topics --profile "$AWS_DEFAULT_PROFILE" --query "Topics[?contains(TopicArn, '${FULL_TOPIC_NAME}')].TopicArn" --output text)

    if [[ -n "$existing_arn" ]]; then
        log "WARNING" "Topic already exists: $existing_arn"
        echo $existing_arn >> "$TOPIC_ARN_FILE"
        echo $existing_arn
    else
        log "INFO" "Creating topic '$FULL_TOPIC_NAME'..."
        # Create the SNS topic if it doesn't exist
        response=$(aws sns create-topic --name "$FULL_TOPIC_NAME" --profile "$AWS_DEFAULT_PROFILE" --output json 2>&1)

        # Extract the TopicArn from the response
        if [[ "$response" == *"arn:aws:sns"* ]]; then
            topic_arn=$(echo $response | jq -r '.TopicArn')
            log "INFO" "Topic created successfully: $topic_arn"
            echo $topic_arn >> "$TOPIC_ARN_FILE"
            echo $topic_arn
        else
            log "ERROR" "Error creating topic: $response"
            exit 1
        fi
    fi
}

# Function to list topics
function list_topics() {
    log "INFO" "Listing all SNS topics..."
    aws sns list-topics --profile "$AWS_DEFAULT_PROFILE" --query 'Topics[*].TopicArn' --output text | tee -a "$LOG_FILE"
}

# Function to subscribe SMS
function subscribe_sms() {
    TOPIC_ARN=$1
    PHONE_NUMBER=$2
    log "INFO" "Subscribing phone number '$PHONE_NUMBER' to topic '$TOPIC_ARN'..."
    response=$(aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sms --notification-endpoint "$PHONE_NUMBER" --profile "$AWS_DEFAULT_PROFILE" 2>&1)
    if [[ "$response" == *"arn:aws:sns"* ]]; then
        log "INFO" "SMS subscription request sent to $PHONE_NUMBER for topic $TOPIC_ARN."
    else
        log "ERROR" "Error subscribing SMS: $response"
    fi
}

# Function to subscribe Email
function subscribe_email() {
    TOPIC_ARN=$1
    EMAIL=$2
    log "INFO" "Subscribing email '$EMAIL' to topic '$TOPIC_ARN'..."
    response=$(aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$EMAIL" --profile "$AWS_DEFAULT_PROFILE" 2>&1)
    if [[ "$response" == *"arn:aws:sns"* ]]; then
        log "INFO" "Email subscription request sent to $EMAIL for topic $TOPIC_ARN."
    else
        log "ERROR" "Error subscribing Email: $response"
    fi
}

# Function to list subscribers
function list_subscribers() {
    TOPIC_ARN=$1
    log "INFO" "Listing subscribers for topic '$TOPIC_ARN'..."
    aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --profile "$AWS_DEFAULT_PROFILE" --query 'Subscriptions[*].{Protocol:Protocol,Endpoint:Endpoint,SubscriptionArn:SubscriptionArn}' --output table | tee -a "$LOG_FILE"
}

# Function to send a message
function send_message() {
    TOPIC_ARN=$1
    MESSAGE=$2
    log "INFO" "Sending message to topic '$TOPIC_ARN'..."
    response=$(aws sns publish --topic-arn "$TOPIC_ARN" --message "$MESSAGE" --profile "$AWS_DEFAULT_PROFILE" 2>&1)
    if [[ "$response" == *"MessageId"* ]]; then
        log "INFO" "Message sent to topic $TOPIC_ARN: $MESSAGE"
    else
        log "ERROR" "Error sending message: $response"
    fi
}

# Function to delete a topic
function delete_topic() {
    TOPIC_ARN=$1
    log "INFO" "Deleting topic '$TOPIC_ARN'..."
    response=$(aws sns delete-topic --topic-arn "$TOPIC_ARN" --profile "$AWS_DEFAULT_PROFILE" 2>&1)
    if [[ -z "$response" ]]; then
        log "INFO" "Topic deleted: $TOPIC_ARN"
    else
        log "ERROR" "Error deleting topic: $response"
    fi
}

# Cleanup any previous ARNs stored in the file
log "INFO" "Cleaning up previous ARN and log files..."
rm -f "$TOPIC_ARN_FILE"
rm -f "$LOG_FILE"

# Check if the profile exists
check_profile

# Read configuration
read_config

# Extract the AWS account ID, region, and sns_topic_prefix from the configuration
AWS_ACCOUNT_ID=$(echo "$CONFIG" | jq -r '.aws_account_id')
REGION=$(echo "$CONFIG" | jq -r '.region')
sns_topic_prefix=$(echo "$CONFIG" | jq -r '.sns_topic_prefix')

# Ensure the topics are valid and non-empty
if [ -z "$(echo "$CONFIG" | jq -r '.topics | keys[]')" ]; then
    log "ERROR" "No topics found in the configuration file."
    exit 1
fi

# Iterate over topics in the configuration
for TOPIC_NAME in $(echo "$CONFIG" | jq -r '.topics | keys[]'); do
    TOPIC_ARN=$(add_topic "$TOPIC_NAME")

    # Subscribe SMS subscribers if the topic type includes SMS
    for PHONE_NUMBER in $(echo "$CONFIG" | jq -r ".topics[\"$TOPIC_NAME\"].sms_subscribers[]"); do
        subscribe_sms "$TOPIC_ARN" "$PHONE_NUMBER"
    done

    # Subscribe Email subscribers if the topic type includes email
    for EMAIL in $(echo "$CONFIG" | jq -r ".topics[\"$TOPIC_NAME\"].email_subscribers[]"); do
        subscribe_email "$TOPIC_ARN" "$EMAIL"
    done

    # List subscribers
    list_subscribers "$TOPIC_ARN"

    # Send a message to the topic
    send_message "$TOPIC_ARN" "This is a test message for ${sns_topic_prefix}${TOPIC_NAME}"
done

# Cleanup: Unsubscribe all subscribers and delete topics
if [ -f "$TOPIC_ARN_FILE" ]; then
    while IFS= read -r TOPIC_ARN; do
        log "INFO" "Unsubscribing and deleting topic '$TOPIC_ARN'..."
        # Unsubscribe all subscribers
        SUBSCRIPTIONS=$(aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --profile "$AWS_DEFAULT_PROFILE" --query 'Subscriptions[*].SubscriptionArn' --output text)
        for SUBSCRIPTION_ARN in $SUBSCRIPTIONS; do
            response=$(aws sns unsubscribe --subscription-arn "$SUBSCRIPTION_ARN" --profile "$AWS_DEFAULT_PROFILE" 2>&1)
            if [[ -z "$response" ]]; then
                log "INFO" "Unsubscribed $SUBSCRIPTION_ARN from $TOPIC_ARN"
            else
                log "ERROR" "Error unsubscribing: $response"
            fi
        done

        # Delete the topic
        delete_topic "$TOPIC_ARN"
    done < "$TOPIC_ARN_FILE"
else
    log "WARNING" "No topics were created or the ARNs were not saved. No cleanup needed."
fi

# Cleanup the ARN file
rm -f "$TOPIC_ARN_FILE"

log "INFO" "Integration test completed successfully."


