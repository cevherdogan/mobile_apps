#!/bin/bash
set -e

# Set the default AWS profile
export AWS_DEFAULT_PROFILE=cevherdogan

# Function to log messages with timestamps
function log() {
    local LEVEL=$1
    shift
    local MESSAGE=$@
    local TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE"
}

# Function to list all SNS topics
function list_topics() {
    log "INFO" "Listing all SNS topics..."
    aws sns list-topics --profile "$AWS_DEFAULT_PROFILE" --query 'Topics[*].TopicArn' --output text
}

# Function to list subscriptions by topic
function list_subscriptions() {
    local TOPIC_ARN=$1
    log "INFO" "Listing subscriptions for topic '$TOPIC_ARN'..."
    aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --profile "$AWS_DEFAULT_PROFILE" --query 'Subscriptions[*].{Protocol:Protocol,Endpoint:Endpoint,SubscriptionArn:SubscriptionArn}' --output table
}

# Function to check for pending confirmations and prompt for action
function check_pending_confirmations() {
    local TOPIC_ARN=$1
    log "INFO" "Checking for pending confirmations for topic '$TOPIC_ARN'..."

    # Get list of pending subscriptions
    PENDING_SUBSCRIPTIONS=$(aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --profile "$AWS_DEFAULT_PROFILE" --query 'Subscriptions[?SubscriptionArn == `PendingConfirmation`].[Protocol,Endpoint]' --output text)

    if [ -z "$PENDING_SUBSCRIPTIONS" ]; then
        log "INFO" "No pending confirmations for topic '$TOPIC_ARN'."
    else
        log "WARNING" "Pending confirmations detected for the following subscriptions:"
        echo "$PENDING_SUBSCRIPTIONS"

        read -p "Do you want to resend confirmation emails? (y/n): " RESEND_CONFIRMATION
        RESEND_CONFIRMATION=${RESEND_CONFIRMATION:-y}  # Default to 'y'
        if [ "$RESEND_CONFIRMATION" == "y" ]; then
            while IFS= read -r SUBSCRIPTION; do
                ENDPOINT=$(echo $SUBSCRIPTION | awk '{print $2}')
                log "INFO" "Resending confirmation to $ENDPOINT..."
                echo "Please manually resend confirmation emails for pending endpoints."
            done <<< "$PENDING_SUBSCRIPTIONS"
        else
            log "INFO" "Skipping confirmation for pending subscriptions."
        fi
    fi
}

# Function to add a new email subscription
function add_email_subscription() {
    local TOPIC_ARN=$1
    local EMAIL=$2
    log "INFO" "Adding email subscription for $EMAIL to topic '$TOPIC_ARN'..."
    aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$EMAIL" --profile "$AWS_DEFAULT_PROFILE"
}

# Function to add a new SMS subscription
function add_sms_subscription() {
    local TOPIC_ARN=$1
    local PHONE_NUMBER=$2
    log "INFO" "Adding SMS subscription for $PHONE_NUMBER to topic '$TOPIC_ARN'..."
    aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sms --notification-endpoint "$PHONE_NUMBER" --profile "$AWS_DEFAULT_PROFILE"
}

# Function to publish a test email message to a topic
function publish_test_email() {
    local TOPIC_ARN=$1
    log "INFO" "Publishing test email message to topic '$TOPIC_ARN'..."
    aws sns publish --topic-arn "$TOPIC_ARN" --message "Test email message" --profile "$AWS_DEFAULT_PROFILE"
}

# Function to publish a test SMS message
function publish_test_sms() {
    local PHONE_NUMBER=$1
    log "INFO" "Publishing test SMS message to phone number '$PHONE_NUMBER'..."
    aws sns publish --phone-number "$PHONE_NUMBER" --message "Test SMS message" --profile "$AWS_DEFAULT_PROFILE"
}

# Main script execution
log "INFO" "Starting simple test validation..."

# List topics
TOPICS=$(list_topics)
echo "Available SNS Topics:"
echo "$TOPICS"

# Prompt the user to enter a topic ARN
read -p "Enter the ARN of the topic to validate: " TOPIC_ARN

# List subscriptions for the selected topic
list_subscriptions "$TOPIC_ARN"

# Prompt to add a new email subscription
read -p "Do you want to add an email subscription? (y/n): " ADD_EMAIL_SUB
ADD_EMAIL_SUB=${ADD_EMAIL_SUB:-y}  # Default to 'y'
if [ "$ADD_EMAIL_SUB" == "y" ]; then
    read -p "Enter the email to subscribe: " EMAIL
    add_email_subscription "$TOPIC_ARN" "$EMAIL"
fi

# Prompt to add a new SMS subscription
read -p "Do you want to add an SMS subscription? (y/n): " ADD_SMS_SUB
ADD_SMS_SUB=${ADD_SMS_SUB:-y}  # Default to 'y'
if [ "$ADD_SMS_SUB" == "y" ]; then
    read -p "Enter the phone number to subscribe (e.g., +14846869923): " PHONE_NUMBER
    add_sms_subscription "$TOPIC_ARN" "$PHONE_NUMBER"
fi

# Check for pending confirmations
check_pending_confirmations "$TOPIC_ARN"

# Ask if the user wants to send a test email
read -p "Do you want to send a test email to this topic? (y/n): " SEND_EMAIL
SEND_EMAIL=${SEND_EMAIL:-y}  # Default to 'y'
if [ "$SEND_EMAIL" == "y" ]; then
    publish_test_email "$TOPIC_ARN"
fi

# Ask if the user wants to send a test SMS
read -p "Do you want to send a test SMS? (y/n): " SEND_SMS
SEND_SMS=${SEND_SMS:-y}  # Default to 'y'
if [ "$SEND_SMS" == "y" ]; then
    read -p "Enter the phone number to send the SMS to (e.g., +14846869923): " PHONE_NUMBER
    publish_test_sms "$PHONE_NUMBER"
fi

log "INFO" "Simple test validation completed."


