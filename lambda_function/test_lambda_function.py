import unittest
from unittest.mock import patch, MagicMock
import json
from lambda_function import (
    lambda_handler,
    create_topic,
    delete_topic,
    subscribe_to_topic,
    unsubscribe_from_topic,
    confirm_subscription,
)

class TestLambdaFunctions(unittest.TestCase):
    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.create_topic")
    @patch("lambda_function.sns_client.set_topic_attributes")
    def test_create_topic_success(
        self, mock_set_topic_attributes, mock_create_topic, mock_retry
    ):
        mock_create_topic.return_value = {"TopicArn": "arn:aws:sns:us-east-1:123456789012:MyTopic"}
        mock_set_topic_attributes.return_value = None
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = create_topic("MyTopic", "MyDisplayName", enable_logging=False)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("TopicArn", json.loads(response["body"]))

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.create_topic")
    def test_create_topic_json_error(self, mock_create_topic, mock_retry):
        mock_create_topic.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = create_topic("MyTopic", "MyDisplayName", enable_logging=False)

        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Geçersiz JSON formatı!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.create_topic")
    def test_create_topic_failure(self, mock_create_topic, mock_retry):
        mock_create_topic.side_effect = Exception("Unexpected error")
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = create_topic("MyTopic", "MyDisplayName", enable_logging=False)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Topic oluşturulurken hata oluştu!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.delete_topic")
    def test_delete_topic_success(self, mock_delete_topic, mock_retry):
        mock_delete_topic.return_value = None
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = delete_topic("arn:aws:sns:us-east-1:123456789012:MyTopic", enable_logging=False)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Topic başarıyla silindi!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.delete_topic")
    def test_delete_topic_json_error(self, mock_delete_topic, mock_retry):
        mock_delete_topic.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = delete_topic("arn:aws:sns:us-east-1:123456789012:MyTopic", enable_logging=False)

        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Geçersiz JSON formatı!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.delete_topic")
    def test_delete_topic_failure(self, mock_delete_topic, mock_retry):
        mock_delete_topic.side_effect = Exception("Unexpected error")
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = delete_topic("arn:aws:sns:us-east-1:123456789012:MyTopic", enable_logging=False)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Topic silinirken hata oluştu!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.subscribe")
    def test_subscribe_to_topic_success(self, mock_subscribe, mock_retry):
        mock_subscribe.return_value = {"SubscriptionArn": "arn:aws:sns:us-east-1:123456789012:MyTopic:1234abcd"}
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = subscribe_to_topic("arn:aws:sns:us-east-1:123456789012:MyTopic", "email", "example@example.com", enable_logging=False)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Abone başarıyla eklendi!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.subscribe")
    def test_subscribe_to_topic_json_error(self, mock_subscribe, mock_retry):
        mock_subscribe.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = subscribe_to_topic("arn:aws:sns:us-east-1:123456789012:MyTopic", "email", "example@example.com", enable_logging=False)

        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Geçersiz JSON formatı!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.subscribe")
    def test_subscribe_to_topic_failure(self, mock_subscribe, mock_retry):
        mock_subscribe.side_effect = Exception("Unexpected error")
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = subscribe_to_topic("arn:aws:sns:us-east-1:123456789012:MyTopic", "email", "example@example.com", enable_logging=False)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Abone eklenirken hata oluştu!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.unsubscribe")
    def test_unsubscribe_from_topic_success(self, mock_unsubscribe, mock_retry):
        mock_unsubscribe.return_value = None
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = unsubscribe_from_topic("arn:aws:sns:us-east-1:123456789012:MyTopic:1234abcd", enable_logging=False)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Abonelik başarıyla iptal edildi!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.unsubscribe")
    def test_unsubscribe_from_topic_json_error(self, mock_unsubscribe, mock_retry):
        mock_unsubscribe.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = unsubscribe_from_topic("arn:aws:sns:us-east-1:123456789012:MyTopic:1234abcd", enable_logging=False)

        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Geçersiz JSON formatı!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.unsubscribe")
    def test_unsubscribe_from_topic_failure(self, mock_unsubscribe, mock_retry):
        mock_unsubscribe.side_effect = Exception("Unexpected error")
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = unsubscribe_from_topic("arn:aws:sns:us-east-1:123456789012:MyTopic:1234abcd", enable_logging=False)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Abonelik iptal edilirken hata oluştu!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.confirm_subscription")
    def test_confirm_subscription_success(self, mock_confirm_subscription, mock_retry):
        mock_confirm_subscription.return_value = None
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = confirm_subscription("token1234", "arn:aws:sns:us-east-1:123456789012:MyTopic", enable_logging=False)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Abonelik başarıyla onaylandı!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.confirm_subscription")
    def test_confirm_subscription_json_error(self, mock_confirm_subscription, mock_retry):
        mock_confirm_subscription.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = confirm_subscription("token1234", "arn:aws:sns:us-east-1:123456789012:MyTopic", enable_logging=False)

        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Geçersiz JSON formatı!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.sns_client.confirm_subscription")
    def test_confirm_subscription_failure(self, mock_confirm_subscription, mock_retry):
        mock_confirm_subscription.side_effect = Exception("Unexpected error")
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)
        response = confirm_subscription("token1234", "arn:aws:sns:us-east-1:123456789012:MyTopic", enable_logging=False)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Abonelik onaylanırken hata oluştu!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.create_topic")
    def test_lambda_handler_create_topic(self, mock_create_topic, mock_retry):
        event = {"action": "create_topic", "topic_name": "MyTopic", "topic_type": "MyDisplayName"}
        mock_create_topic.return_value = {
            "statusCode": 200,
            "body": json.dumps({"message": "Topic başarıyla oluşturuldu!"}),
        }
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Topic başarıyla oluşturuldu!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.delete_topic")
    def test_lambda_handler_delete_topic(self, mock_delete_topic, mock_retry):
        event = {"action": "delete_topic", "topic_arn": "arn:aws:sns:us-east-1:123456789012:MyTopic"}
        mock_delete_topic.return_value = {
            "statusCode": 200,
            "body": json.dumps({"message": "Topic başarıyla silindi!"}),
        }
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Topic başarıyla silindi!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.subscribe_to_topic")
    def test_lambda_handler_subscribe(self, mock_subscribe_to_topic, mock_retry):
        event = {
            "action": "subscribe",
            "topic_arn": "arn:aws:sns:us-east-1:123456789012:MyTopic",
            "protocol": "email",
            "endpoint": "example@example.com",
        }
        mock_subscribe_to_topic.return_value = {
            "statusCode": 200,
            "body": json.dumps({"message": "Abone başarıyla eklendi!"}),
        }
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Abone başarıyla eklendi!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.unsubscribe_from_topic")
    def test_lambda_handler_unsubscribe(self, mock_unsubscribe_from_topic, mock_retry):
        event = {"action": "unsubscribe", "subscription_arn": "arn:aws:sns:us-east-1:123456789012:MyTopic:1234abcd"}
        mock_unsubscribe_from_topic.return_value = {
            "statusCode": 200,
            "body": json.dumps({"message": "Abonelik başarıyla iptal edildi!"}),
        }
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Abonelik başarıyla iptal edildi!", json.loads(response["body"])["message"])

    @patch("lambda_function.exponential_backoff_retry")
    @patch("lambda_function.confirm_subscription")
    def test_lambda_handler_confirm_subscription(self, mock_confirm_subscription, mock_retry):
        event = {"action": "confirm_subscription", "token": "token1234", "topic_arn": "arn:aws:sns:us-east-1:123456789012:MyTopic"}
        mock_confirm_subscription.return_value = {
            "statusCode": 200,
            "body": json.dumps({"message": "Abonelik başarıyla onaylandı!"}),
        }
        mock_retry.side_effect = lambda func, *args, **kwargs: func(*args, **kwargs)

        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Abonelik başarıyla onaylandı!", json.loads(response["body"])["message"])

    def test_lambda_handler_invalid_action(self):
        event = {"action": "invalid_action"}
        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 400)
        self.assertIn("Geçersiz işlem!", json.loads(response["body"])["message"])


if __name__ == "__main__":
    unittest.main()

