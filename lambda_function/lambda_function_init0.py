import boto3
import json
import os

sns_client = boto3.client('sns')


def log_message(message, enable_logging):
    if enable_logging:
        print(message)


def create_topic(topic_name, topic_type, enable_logging):
    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']

        if topic_type:
            sns_client.set_topic_attributes(
                TopicArn=topic_arn,
                AttributeName='DisplayName',
                AttributeValue=topic_type
            )

        log_message(f"Topic created: {topic_arn}", enable_logging)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Topic {topic_name} başarıyla oluşturuldu!',
                'TopicArn': topic_arn
            })
        }
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Geçersiz JSON formatı!',
                'error': str(e)
            })
        }
    except Exception as e:
        log_message(f"Error creating topic: {str(e)}", enable_logging)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Topic oluşturulurken hata oluştu!',
                'error': str(e)
            })
        }


def delete_topic(topic_arn, enable_logging):
    try:
        sns_client.delete_topic(TopicArn=topic_arn)
        log_message(f"Topic deleted: {topic_arn}", enable_logging)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Topic {topic_arn} başarıyla silindi!'
            })
        }
    except json.JSONDecodeError as e:
        log_message(f"JSON decoding error: {str(e)}", enable_logging)
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Geçersiz JSON formatı!',
                'error': str(e)
            })

