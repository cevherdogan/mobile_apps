from flask import Blueprint, render_template, request, jsonify
from .sns_utils import list_topics, publish_to_topic

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    profile_name = 'cevherdogan'
    region_name = 'us-east-1'

    # Load topics
    topics = list_topics(profile_name, region_name)

    # Categorize topics
    sms_topics = [topic['TopicArn'] for topic in topics if 'sms' in topic['TopicArn']]
    email_topics = [topic['TopicArn'] for topic in topics if 'email' in topic['TopicArn']]
    mixed_topics = [topic['TopicArn'] for topic in topics if 'mixed' in topic['TopicArn']]

    if request.method == 'POST':
        topic_arn = request.form['topic_arn']
        message = request.form['message']
        response = publish_to_topic(topic_arn, message, profile_name, region_name)
        return render_template('index.html', sms_topics=sms_topics, email_topics=email_topics, mixed_topics=mixed_topics, response=response)

    return render_template('index.html', sms_topics=sms_topics, email_topics=email_topics, mixed_topics=mixed_topics)

