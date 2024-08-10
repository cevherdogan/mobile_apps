#!/bin/bash
set -e

# Set the default AWS profile
export AWS_DEFAULT_PROFILE=cevherdogan

CONFIG_FILE="sns_config.json"
TOPIC_ARN_FILE="topic_arns.txt"

# Function to check if the profile exists
function check_profile() {
    if ! aws configure list-profiles | grep -q "^$AWS_DEFAULT_PROFILE$"; then
        echo "Error: The config profile '$AWS_DEFAULT_PROFILE' could not be found."
        exit 1
    fi
}

# Function to read the configuration file
function read_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: Configuration file $CONFIG_FILE not found."
        exit 1
    fi
    CONFIG=$(cat "$CONFIG_FILE")
}

# Function to add a topic
function add_topic() {
    TOPIC_NAME=$1
    response=$(aws sns create-topic --name "$TOPIC_NAME" 2>&1)

    if [[ "$response" == *"arn:aws:sns"* ]]; then
        topic_arn=$(echo $response | jq -r '.TopicArn')
        echo "Topic created: $topic_arn"
        echo $topic_arn >> "$TOPIC_ARN_FILE"
        echo $topic_arn
    else
        echo "Error creating topic: $response"
        exit 1
    fi
}

# Function to list topics
function list_topics() {
    aws sns list-topics --query 'Topics[*].TopicArn' --output text
}

# Function to subscribe SMS
function subscribe_sms() {
    TOPIC_ARN=$1
    PHONE_NUMBER=$2
    aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sms --notification-endpoint "$PHONE_NUMBER"
    echo "SMS subscription request sent to $PHONE_NUMBER for topic $TOPIC_ARN."
}

# Function to subscribe Email
function subscribe_email() {
    TOPIC_ARN=$1
    EMAIL=$2
    aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$EMAIL"
    echo "Email subscription request sent to $EMAIL for topic $TOPIC_ARN."
}

# Function to list subscribers
function list_subscribers() {
    TOPIC_ARN=$1
    aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --query 'Subscriptions[*].{Protocol:Protocol,Endpoint:Endpoint,SubscriptionArn:SubscriptionArn}' --output table
}

# Function to send a message
function send_message() {
    TOPIC_ARN=$1
    MESSAGE=$2
    aws sns publish --topic-arn "$TOPIC_ARN" --message "$MESSAGE"
    echo "Message sent to topic $TOPIC_ARN: $MESSAGE"
}

# Function to delete a topic
function delete_topic() {
    TOPIC_ARN=$1
    aws sns delete-topic --topic-arn "$TOPIC_ARN"
    echo "Topic deleted: $TOPIC_ARN"
}

# Cleanup any previous ARNs stored in the file
rm -f "$TOPIC_ARN_FILE"

# Check if the profile exists
check_profile

# Read configuration
read_config

# Iterate over topics in the configuration
for TOPIC_NAME in $(echo "$CONFIG" | jq -r '.topics | keys[]'); do
    TOPIC_ARN=$(add_topic "$TOPIC_NAME")

    # Subscribe SMS subscribers
    for PHONE_NUMBER in $(echo "$CONFIG" | jq -r ".topics[\"$TOPIC_NAME\"].sms_subscribers[]"); do
        subscribe_sms "$TOPIC_ARN" "$PHONE_NUMBER"
    done

    # Subscribe Email subscribers
    for EMAIL in $(echo "$CONFIG" | jq -r ".topics[\"$TOPIC_NAME\"].email_subscribers[]"); do
        if [[ "$TOPIC_NAME" == "MySMSTopic" ]]; then
            echo "Expected failure: Attempting to add an email ($EMAIL) to SMS-only topic ($TOPIC_NAME)"
            subscribe_email "$TOPIC_ARN" "$EMAIL" && echo "Error: Email subscription should have failed" || echo "Passed: Email subscription failed as expected"
        else
            subscribe_email "$TOPIC_ARN" "$EMAIL"
        fi
    done

    # List subscribers
    list_subscribers "$TOPIC_ARN"

    # Send a message to the topic
    send_message "$TOPIC_ARN" "This is a test message for $TOPIC_NAME"
done

# Cleanup: Unsubscribe all subscribers and delete topics
while IFS= read -r TOPIC_ARN; do
    # Unsubscribe all subscribers
    SUBSCRIPTIONS=$(aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --query 'Subscriptions[*].SubscriptionArn' --output text)
    for SUBSCRIPTION_ARN in $SUBSCRIPTIONS; do
        aws sns unsubscribe --subscription-arn "$SUBSCRIPTION_ARN"
        echo "Unsubscribed $SUBSCRIPTION_ARN from $TOPIC_ARN"
    done

    # Delete the topic
    delete_topic "$TOPIC_ARN"
done < "$TOPIC_ARN_FILE"

# Cleanup the ARN file
rm -f "$TOPIC_ARN_FILE"

echo "Integration test completed successfully."


