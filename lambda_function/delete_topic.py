import boto3
import json
import os

sns_client = boto3.client('sns')


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
