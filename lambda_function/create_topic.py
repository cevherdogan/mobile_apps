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
