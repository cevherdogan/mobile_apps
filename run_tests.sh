#!/bin/bash

# Set a flag to exit if any command fails
set -e

echo "Starting unit tests..."

# Run tests in a specific order
echo "Running tests for ConfigManager..."
pytest tests/test_config_manager.py

echo "Running tests for TopicManager..."
pytest tests/test_topic_manager.py

echo "Running tests for NotificationManager..."
pytest tests/test_notification_manager.py


# selective test 
pytest tests/test_topic_manager.py::TestTopicManager::test_create_topic


echo "All tests executed successfully!"


