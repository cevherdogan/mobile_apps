from flask import Blueprint, render_template, request, jsonify
from .sns_utils import list_topics, publish_to_topic, subscribe_to_topic, unsubscribe_from_topic, list_subscriptions_by_topic

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    profile_name = 'cevherdogan'
    region_name = 'us-east-1'

    # Load topics
    topics = list_topics(profile_name, region_name)

    # Categorize topics
    sms_topics = [topic for topic in topics if 'sms' in topic.lower()]
    email_topics = [topic for topic in topics if 'email' in topic.lower()]
    mixed_topics = [topic for topic in topics if 'mixed' in topic.lower()]
    uncategorized_topics = [topic for topic in topics if topic not in sms_topics + email_topics + mixed_topics]

    if request.method == 'POST':
        action = request.form.get('action')
        topic_arn = request.form.get('topic_arn')  # Retrieve topic_arn from the form

        # Print or log the topic_arn for debugging
        print(f"Debug: TopicArn received - {topic_arn}")

        if not topic_arn:
            return "Error: TopicArn is required", 400

        if action == 'publish':
            message = request.form['message']
            response = publish_to_topic(topic_arn, message, profile_name, region_name)
            return render_template('index.html', sms_topics=sms_topics, email_topics=email_topics, mixed_topics=mixed_topics, uncategorized_topics=uncategorized_topics, response=response)

        elif action == 'subscribe':
            protocol = request.form['protocol']
            endpoint = request.form['endpoint']
            response = subscribe_to_topic(topic_arn, protocol, endpoint, profile_name, region_name)
            return render_template('index.html', sms_topics=sms_topics, email_topics=email_topics, mixed_topics=mixed_topics, uncategorized_topics=uncategorized_topics, response=response)

        elif action == 'unsubscribe':
            subscription_arn = request.form['subscription_arn']
            response = unsubscribe_from_topic(subscription_arn, profile_name, region_name)
            return render_template('index.html', sms_topics=sms_topics, email_topics=email_topics, mixed_topics=mixed_topics, uncategorized_topics=uncategorized_topics, response=response)

    return render_template('index.html', sms_topics=sms_topics, email_topics=email_topics, mixed_topics=mixed_topics, uncategorized_topics=uncategorized_topics)

@main.route('/subscriptions', methods=['GET'])
def subscriptions():
    profile_name = 'cevherdogan'
    region_name = 'us-east-1'
    topic_arn = request.args.get('topic_arn')
    
    if not topic_arn:
        return "Error: TopicArn is required", 400
    
    subscriptions = list_subscriptions_by_topic(topic_arn, profile_name, region_name)
    return render_template('subscriptions.html', subscriptions=subscriptions, topic_arn=topic_arn)


