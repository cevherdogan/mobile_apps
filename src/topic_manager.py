import boto3

class TopicManager:
    def __init__(self, config_manager):
        self.config = config_manager.load_config()
        self.sns_client = boto3.client(
            'sns',
            region_name=self.config['aws']['region'],
            aws_access_key_id=self.config['aws']['access_key'],
            aws_secret_access_key=self.config['aws']['secret_key']
        )

    def create_topic(self, topic_name, attributes=None):
        """Belirtilen adla yeni bir SNS topiği oluşturur."""
        response = self.sns_client.create_topic(Name=topic_name, Attributes=attributes or {})
        print(f"Topic created: {response['TopicArn']}")
        return response['TopicArn']

    def delete_topic(self, topic_arn):
        """Belirtilen ARN'e sahip topiği siler."""
        self.sns_client.delete_topic(TopicArn=topic_arn)
        print(f"Topic deleted: {topic_arn}")

    def list_topics(self):
        """Mevcut tüm topikleri ve bu topiklere ait abonelikleri listeler."""
        response = self.sns_client.list_topics()
        topics = response.get('Topics', [])
        for topic in topics:
            print(f"Topic ARN: {topic['TopicArn']}")
            self.list_subscriptions(topic['TopicArn'])

    def add_subscription(self, topic_arn, subscription_type, endpoint):
        """Belirtilen topiğe bir abonelik ekler."""
        response = self.sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=subscription_type,
            Endpoint=endpoint
        )
        print(f"Subscription added: {response['SubscriptionArn']}")

    def list_subscriptions(self, topic_arn):
        """Belirtilen topiğe ait abonelikleri listeler."""
        response = self.sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
        subscriptions = response.get('Subscriptions', [])
        for sub in subscriptions:
            print(f"  Subscription ARN: {sub['SubscriptionArn']}, Endpoint: {sub['Endpoint']}")

    def check_empty_topics(self):
        """Mevcut topikleri kontrol eder ve aboneliği olmayanları tespit eder."""
        response = self.sns_client.list_topics()
        topics = response.get('Topics', [])
        for topic in topics:
            subscriptions = self.sns_client.list_subscriptions_by_topic(TopicArn=topic['TopicArn'])
            if not subscriptions.get('Subscriptions'):
                print(f"Empty topic found: {topic['TopicArn']}")


