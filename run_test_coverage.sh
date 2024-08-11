#!/bin/bash
set -e

echo "Starting unit tests with coverage..."

pytest --cov=src tests/test_config_manager.py
pytest --cov=src tests/test_topic_manager.py
pytest --cov=src tests/test_notification_manager.py

echo "All tests executed successfully with coverage!"


