from flask import Blueprint, request, jsonify
from .sns_utils import list_topics, publish_to_topic, subscribe_to_topic, unsubscribe_from_topic

main = Blueprint('main', __name__)

@main.route('/topics', methods=['GET'])
def get_topics():
    profile_name = request.args.get('profile', 'default')
    region_name = request.args.get('region', 'us-east-1')
    topics = list_topics(profile_name, region_name)
    return jsonify(topics)

@main.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    topic_arn = data['topic_arn']
    message = data['message']
    profile_name = data.get('profile', 'default')
    region_name = data.get('region', 'us-east-1')
    response = publish_to_topic(topic_arn, message, profile_name, region_name)
    return jsonify(response)

@main.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    topic_arn = data['topic_arn']
    protocol = data['protocol']
    endpoint = data['endpoint']
    profile_name = data.get('profile', 'default')
    region_name = data.get('region', 'us-east-1')
    response = subscribe_to_topic(topic_arn, protocol, endpoint, profile_name, region_name)
    return jsonify(response)

@main.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.get_json()
    subscription_arn = data['subscription_arn']
    profile_name = data.get('profile', 'default')
    region_name = data.get('region', 'us-east-1')
    response = unsubscribe_from_topic(subscription_arn, profile_name, region_name)
    return jsonify(response)


