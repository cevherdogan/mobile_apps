import boto3
import json
import os

sns_client = boto3.client('sns')


def confirm_subscription(token, topic_arn):
    enable_logging = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'

    def log(message):
        if enable_logging:
            print(message)

    try:
        sns_client.confirm_subscription(
            TopicArn=topic_arn,
            Token=token,
            AuthenticateOnUnsubscribe='true'
        )
        log(
            f"Subscription confirmed for {topic_arn} "
            f"with token {token}"
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Abonelik {topic_arn} başarıyla onaylandı!'
            })
        }
    except json.JSONDecodeError as e:
        log(f"JSON decoding error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Geçersiz JSON formatı!',
                'error': str(e)
            })
        }
    except Exception as e:
        log(f"Error confirming subscription: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Abonelik onaylanırken hata oluştu!',
                'error': str(e)
            })
        }
