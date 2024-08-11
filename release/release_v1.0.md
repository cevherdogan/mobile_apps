# v1.0 - Initial SNS Subscription Manager

**Release Date:** 2024-08-10

## Summary

This release marks the initial version of the SNS Subscription Manager web application. The application provides a user-friendly interface to manage Amazon SNS topics, allowing users to post messages, manage subscriptions, and view current subscriptions for different SNS topics. This version focuses on foundational features for handling SNS topic interactions, including support for SMS, Email, and Mixed topic types.

## Features

1. **Topic Management:**
   - Users can select an SNS topic from a dropdown list categorized by SMS, Email, or Mixed types.
   - Users can post messages directly to the selected SNS topic.

2. **Subscription Management:**
   - Users can subscribe to topics using either SMS or Email protocols.
   - Subscriptions can be managed (subscribed/unsubscribed) directly from the web interface.
   - Users can view the current list of subscriptions for each topic, with a clear display of pending confirmations.

3. **Auto-Confirm Feature (Planned for Next Release):**
   - A basic framework has been laid for an auto-confirm feature, which will allow users to automatically confirm pending subscriptions. This feature will be fully implemented in the next release.

## Improvements and Bug Fixes

- **Fixed Issues with TopicArn Handling:**
  - Ensured that the `TopicArn` is correctly passed and handled across all routes.
  - Addressed issues where `TopicArn` was missing, causing errors in managing subscriptions.
  
- **Enhanced User Interface:**
  - Provided a clean and intuitive interface for managing SNS topics and subscriptions.
  - Improved form handling to ensure that the correct topic is selected and used in all operations.

- **Debugging and Error Handling:**
  - Added debugging information to help trace issues related to `TopicArn`.
  - Implemented basic error handling for missing or invalid `TopicArn` values.

## Known Issues

- **Auto-Confirm Feature:** The auto-confirm feature for pending subscriptions is planned but not yet fully functional. The foundation is in place and will be completed in the next release.

- **Subscription Confirmation:** Users must currently manually confirm subscriptions via the SNS console or email; the planned auto-confirm feature will streamline this process.

## Next Steps

- **Mobile App - DRAFT:** Add mobile app draft with React Native for Full Stack Engineering Effort including AWS Infra Automation in Scope
- **Auto-Confirm Implementation:** Complete the auto-confirm feature to automatically handle pending subscriptions.
- **Error Handling Enhancements:** Improve error handling and logging to better manage edge cases and failed operations.
- **Extended SNS Features:** Add support for more advanced SNS features, such as subscription filtering policies and topic attributes.

