#!/bin/bash

curl -X GET http://127.0.0.1:5000/

# Make sure your Flask app is running before executing these commands.

# Replace placeholder values like topic_arn_value, email@example.com, and +1234567890 with actual values relevant to your SNS setup.

#cloudruple:tests cevherdogan$ ../awsops/sns/list_topics.sh
#arn:aws:sns:us-east-1:491169136155:cloudruple-wp-dev-notification-topic arn:aws:sns:us-east-1:491169136155:cpptopic     arn:aws:sns:us-east-1:491169136155:test_routable_MyFirstTopic        arn:aws:sns:us-east-1:491169136155:test_routable_MySMSTopic     arn:aws:sns:us-east-1:491169136155:test_routable_email_topic1   arn:aws:sns:us-east-1:491169136155:test_routable_mixed_topic1        arn:aws:sns:us-east-1:491169136155:test_routable_sns_topic1

curl -X POST http://127.0.0.1:5000/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "action=publish&topic_arn=topic_arn_value&message=This is a test message"

# Subscribe an Email to a Topic

curl -X POST http://127.0.0.1:5000/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "action=subscribe&topic_arn=topic_arn_value&protocol=email&endpoint=email@example.com"

# Subscribe a Phone Number to a Topic (SMS)

curl -X POST http://127.0.0.1:5000/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "action=subscribe&topic_arn=topic_arn_value&protocol=sms&endpoint=+1234567890"


# View Subscriptions for a Topic

curl -X GET "http://127.0.0.1:5000/subscriptions?topic_arn=topic_arn_value"


# Unsubscribe from a Topic

curl -X POST http://127.0.0.1:5000/ \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "action=unsubscribe&subscription_arn=subscription_arn_value"


# Auto-Confirm Pending Subscriptions

curl -X POST http://127.0.0.1:5000/auto_confirm \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "topic_arn=topic_arn_value"






