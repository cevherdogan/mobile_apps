import boto3
import json
import os

sns_client = boto3.client('sns')

def create_topic(topic_name, topic_type):
    enable_logging = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'

    def log(message):
        if enable_logging:
            print(message)

    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']

        if topic_type:
            sns_client.set_topic_attributes(
                TopicArn=topic_arn,
                AttributeName='DisplayName',
                AttributeValue=topic_type
            )

        log(f"Topic created: {topic_arn}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Topic {topic_name} başarıyla oluşturuldu!',
                'TopicArn': topic_arn
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
        log(f"Error creating topic: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Topic oluşturulurken hata oluştu!',
                'error': str(e)
            })
        }

def delete_topic(topic_arn):
    enable_logging = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'

    def log(message):
        if enable_logging:
            print(message)

    try:
        sns_client.delete_topic(TopicArn=topic_arn)
        log(f"Topic deleted: {topic_arn}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Topic {topic_arn} başarıyla silindi!'
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
        log(f"Error deleting topic: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Topic silinirken hata oluştu!',
                'error': str(e)
            })
        }

def subscribe_to_topic(topic_arn, protocol, endpoint):
    enable_logging = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'

    def log(message):
        if enable_logging:
            print(message)

    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
            ReturnSubscriptionArn=True
        )
        subscription_arn = response['SubscriptionArn']
        log(f"Subscription added: {subscription_arn} to {topic_arn}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Abone {endpoint} başarıyla eklendi!',
                'SubscriptionArn': subscription_arn
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
        log(f"Error subscribing to topic: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Abone eklenirken hata oluştu!',
                'error': str(e)
            })
        }

def unsubscribe_from_topic(subscription_arn):
    enable_logging = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'

    def log(message):
        if enable_logging:
            print(message)

    try:
        sns_client.unsubscribe(SubscriptionArn=subscription_arn)
        log(f"Subscription removed: {subscription_arn}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Abonelik {subscription_arn} başarıyla iptal edildi!'
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
        log(f"Error unsubscribing from topic: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Abonelik iptal edilirken hata oluştu!',
                'error': str(e)
            })
        }

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
        log(f"Subscription confirmed for {topic_arn} with token {token}")
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

def lambda_handler(event, context):
    action = event.get('action')
    enable_logging = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'

    def log(message):
        if enable_logging:
            print(message)

    try:
        if action == 'create_topic':
            return create_topic(event.get('topic_name'), event.get('topic_type'))
        elif action == 'delete_topic':
            return delete_topic(event.get('topic_arn'))
        elif action == 'subscribe':
            return subscribe_to_topic(event.get('topic_arn'), event.get('protocol'), event.get('endpoint'))
        elif action == 'unsubscribe':
            return unsubscribe_from_topic(event.get('subscription_arn'))
        elif action == 'confirm_subscription':
            return confirm_subscription(event.get('token'), event.get('topic_arn'))
        else:
            log("Invalid action")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Geçersiz işlem!'})
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
        log(f"Unhandled error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Bilinmeyen bir hata oluştu!',
                'error': str(e)
            })
        }


