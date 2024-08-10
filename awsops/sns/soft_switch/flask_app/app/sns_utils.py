import boto3
from botocore.exceptions import ClientError

import boto3

def list_topics(profile_name, region_name):
    session = boto3.Session(profile_name=profile_name)
    sns = session.client('sns', region_name=region_name)
    return sns.list_topics()['Topics']

def publish_to_topic(topic_arn, message, profile_name, region_name):
    session = boto3.Session(profile_name=profile_name)
    sns = session.client('sns', region_name=region_name)
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return response

def subscribe_to_topic(topic_arn, protocol, endpoint, profile_name, region_name):
    session = boto3.Session(profile_name=profile_name)
    sns = session.client('sns', region_name=region_name)
    try:
        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
            ReturnSubscriptionArn=True
        )
        return response
    except ClientError as e:
        return str(e)

def unsubscribe_from_topic(subscription_arn, profile_name, region_name):
    session = boto3.Session(profile_name=profile_name)
    sns = session.client('sns', region_name=region_name)
    try:
        response = sns.unsubscribe(
            SubscriptionArn=subscription_arn
        )
        return response
    except ClientError as e:
        return str(e)


