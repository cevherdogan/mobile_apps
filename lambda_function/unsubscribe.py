import boto3
import json
import os

sns_client = boto3.client("sns")


def unsubscribe_from_topic(subscription_arn):
    enable_logging = os.getenv("ENABLE_LOGGING", "false").lower() == "true"

    def log(message):
        if enable_logging:
            print(message)

    try:
        sns_client.unsubscribe(SubscriptionArn=subscription_arn)
        log(f"Subscription removed: {subscription_arn}", enable_logging)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": f"Abonelik {subscription_arn} başarıyla iptal edildi!"}
            ),
        }
    except json.JSONDecodeError as e:
        log(f"JSON decoding error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log(f"Error unsubscribing from topic: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Abonelik iptal edilirken hata oluştu!", "error": str(e)}
            ),
        }
