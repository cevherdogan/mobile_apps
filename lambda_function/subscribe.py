import boto3
import json
import os

sns_client = boto3.client("sns")


def subscribe_to_topic(topic_arn, protocol, endpoint):
    enable_logging = os.getenv("ENABLE_LOGGING", "false").lower() == "true"

    def log(message):
        if enable_logging:
            print(message)

    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
            ReturnSubscriptionArn=True,
        )
        subscription_arn = response["SubscriptionArn"]
        log(
            f"Subscription added: {subscription_arn} " f"to {topic_arn}", enable_logging
        )
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": f"Abone {endpoint} başarıyla eklendi!",
                    "SubscriptionArn": subscription_arn,
                }
            ),
        }
    except json.JSONDecodeError as e:
        log(f"JSON decoding error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log(f"Error subscribing to topic: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Abone eklenirken hata oluştu!", "error": str(e)}
            ),
        }
