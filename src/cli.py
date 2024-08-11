import argparse
from topic_manager import TopicManager
from config_manager import ConfigManager
from notification_manager import NotificationManager

def main():
    parser = argparse.ArgumentParser(description="Manage AWS SNS topics and subscriptions")
    
    parser.add_argument("command", help="Command to run", choices=["create_topic", "add_subscription", "list_topics", "check_empty_topics", "configure_notifications"])
    parser.add_argument("--topic_name", help="Name of the topic")
    parser.add_argument("--subscription_type", help="Subscription type (email or sns)")
    parser.add_argument("--endpoint", help="Subscription endpoint (email address or sns ARN)")
    parser.add_argument("--reminder_days", nargs='+', type=int, help="Days to send reminders")
    parser.add_argument("--deletion_days", type=int, help="Days after which empty topic is deleted")
    
    args = parser.parse_args()
    
    config_manager = ConfigManager("config/config.yaml")
    topic_manager = TopicManager(config_manager)
    notification_manager = NotificationManager(config_manager)
    
    if args.command == "create_topic":
        if args.topic_name:
            topic_manager.create_topic(args.topic_name)
        else:
            print("Error: --topic_name is required for create_topic")
    
    elif args.command == "add_subscription":
        if args.topic_name and args.subscription_type and args.endpoint:
            topic_manager.add_subscription(args.topic_name, args.subscription_type, args.endpoint)
        else:
            print("Error: --topic_name, --subscription_type and --endpoint are required for add_subscription")
    
    elif args.command == "list_topics":
        topic_manager.list_topics()
    
    elif args.command == "check_empty_topics":
        topic_manager.check_empty_topics()
    
    elif args.command == "configure_notifications":
        if args.reminder_days and args.deletion_days:
            notification_manager.configure_notification_schedule(args.reminder_days, args.deletion_days)
        else:
            print("Error: --reminder_days and --deletion_days are required for configure_notifications")
    
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()

