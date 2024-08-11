import boto3
import json
import os
import time
from botocore.exceptions import ClientError, EndpointConnectionError

sns_client = boto3.client("sns")

# Maksimum deneme sayısı ve timeout sürelerini belirleyelim
MAX_RETRIES = 5
TIMEOUT = 5  # saniye


def log_message(message, enable_logging):
    if enable_logging:
        print(message)


def exponential_backoff_retry(func, *args, **kwargs):
    """Exponential backoff ile bir işlevi tekrar dener."""
    enable_logging = kwargs.get("enable_logging", False)
    retries = 0
    while retries < MAX_RETRIES:
        try:
            return func(*args, **kwargs)
        except (ClientError, EndpointConnectionError) as e:
            wait_time = 2**retries
            log_message(
                f"Hata: {str(e)}, {wait_time} saniye sonra tekrar denenecek...",
                enable_logging,
            )
            time.sleep(wait_time)
            retries += 1
    raise Exception("Maksimum deneme sayısına ulaşıldı")


def create_topic(topic_name, topic_type, enable_logging):
    def _create():
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response["TopicArn"]

        if topic_type:
            sns_client.set_topic_attributes(
                TopicArn=topic_arn,
                AttributeName="DisplayName",
                AttributeValue=topic_type,
            )

        log_message(f"Topic created: {topic_arn}", enable_logging)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": f"Topic {topic_name} başarıyla oluşturuldu!",
                    "TopicArn": topic_arn,
                }
            ),
        }

    try:
        return exponential_backoff_retry(_create, enable_logging=enable_logging)
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log_message(f"Error creating topic: {str(e)}", enable_logging)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Topic oluşturulurken hata oluştu!", "error": str(e)}
            ),
        }


def delete_topic(topic_arn, enable_logging):
    def _delete():
        sns_client.delete_topic(TopicArn=topic_arn)
        log_message(f"Topic deleted: {topic_arn}", enable_logging)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Topic {topic_arn} başarıyla silindi!"}),
        }

    try:
        return exponential_backoff_retry(_delete, enable_logging=enable_logging)
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log_message(f"Error deleting topic: {str(e)}", enable_logging)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Topic silinirken hata oluştu!", "error": str(e)}
            ),
        }


def subscribe_to_topic(topic_arn, protocol, endpoint, enable_logging):
    def _subscribe():
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
            ReturnSubscriptionArn=True,
        )
        subscription_arn = response["SubscriptionArn"]
        log_message(
            f"Subscription added: {subscription_arn} to {topic_arn}",
            enable_logging,
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

    try:
        return exponential_backoff_retry(_subscribe, enable_logging=enable_logging)
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log_message(f"Error subscribing to topic: {str(e)}", enable_logging)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Abone eklenirken hata oluştu!", "error": str(e)}
            ),
        }


def unsubscribe_from_topic(subscription_arn, enable_logging):
    def _unsubscribe():
        sns_client.unsubscribe(SubscriptionArn=subscription_arn)
        log_message(f"Subscription removed: {subscription_arn}", enable_logging)
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": f"Abonelik {subscription_arn} başarıyla iptal edildi!"}
            ),
        }

    try:
        return exponential_backoff_retry(_unsubscribe, enable_logging=enable_logging)
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log_message(f"Error unsubscribing from topic: {str(e)}", enable_logging)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Abonelik iptal edilirken hata oluştu!", "error": str(e)}
            ),
        }


def confirm_subscription(token, topic_arn, enable_logging):
    def _confirm():
        sns_client.confirm_subscription(
            TopicArn=topic_arn,
            Token=token,
            AuthenticateOnUnsubscribe="true",
        )
        log_message(
            f"Subscription confirmed for {topic_arn} with token {token}",
            enable_logging,
        )
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": f"Abonelik {topic_arn} başarıyla onaylandı!"}
            ),
        }

    try:
        return exponential_backoff_retry(_confirm, enable_logging=enable_logging)
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log_message(f"Error confirming subscription: {str(e)}", enable_logging)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Abonelik onaylanırken hata oluştu!", "error": str(e)}
            ),
        }


def lambda_handler(event, context):
    action = event.get("action")
    enable_logging = os.getenv("ENABLE_LOGGING", "false").lower() == "true"

    try:
        if action == "create_topic":
            return create_topic(
                event.get("topic_name"), event.get("topic_type"), enable_logging
            )
        elif action == "delete_topic":
            return delete_topic(event.get("topic_arn"), enable_logging)
        elif action == "subscribe":
            return subscribe_to_topic(
                event.get("topic_arn"),
                event.get("protocol"),
                event.get("endpoint"),
                enable_logging,
            )
        elif action == "unsubscribe":
            return unsubscribe_from_topic(event.get("subscription_arn"), enable_logging)
        elif action == "confirm_subscription":
            return confirm_subscription(
                event.get("token"), event.get("topic_arn"), enable_logging
            )
        else:
            log_message("Invalid action", enable_logging)
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Geçersiz işlem!"}),
            }
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Geçersiz JSON formatı!", "error": str(e)}),
        }
    except Exception as e:
        log_message(f"Unhandled error: {str(e)}", enable_logging)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Bilinmeyen bir hata oluştu!", "error": str(e)}
            ),
        }
