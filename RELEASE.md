# Release Notes

This file tracks the tags and the associated changes in the project.

| Version | Date       | Summary                                                                 |
|---------|------------|-------------------------------------------------------------------------|
| v1.3.0 | 2024-08-11 | Added optional logging to Lambda function and enhanced error handling. Default logging set to False. Updated memory and timeout settings in deployment script. |
| v1.2 | 2024-08-10 | Hangi Topik de hangi üyelik var problem vardı çözüldü |
| v1.1 | 2024-08-10 | Added create_test_topics.sh, masked soft_switch/config/sns_config.json added sample jinja2 template to illustrate the expected format and values for it |
| v1.0 | 2024-08-10 | Added automated tagging and supplemental script to help develop release letter |

## Summary of Changes
### v1.3.0

- Added optional logging to Lambda function and enhanced error handling. Default logging set to False. Updated memory and timeout settings in deployment script. (f9eed89)
- TDD icin basit bir lambda fonksiyonu ve gerekli scriptler (5dc8046)
- Reviewed mobile app dwqev tech stack to pick from. (4590e39)
- Added release to hold releases in md - TODO: Automate using CLI (c697f38)
- Added curl tests for the implemented functionalities, exposed through REST web service endpoint (8510d87)

### v1.2

- Hangi Topik de hangi üyelik var problem vardı çözüldü (efe9d57)
- Fixed topic_arn issues in index.html and routes.py. Confirmed subscription, posting worked thru webapp, view does not (a3d4dea)
- Successfully tested basic UI operation to bring pull down based on topic type and publish messages to them (eacbc87)
- Added Flask app as sample with routes and required APIs to list types of SNS topics and enable posting to them (da89864)

### v1.1

- Added create_test_topics.sh, masked soft_switch/config/sns_config.json added sample jinja2 template to illustrate the expected format and values for it (185cb7f)
- Added Jinja2 template for restore_config.yaml and updated README with generation instructions (43ad563)
- Added topic cleanup for test topics from config (0ba0277)
- Fixed update_release.py and cleaned up RELEASE.md for v1.0 (3acbd8c)


### v1.0

- Added automated tagging and supplemental script to help develop release letter (f055554)
- Updated README and added documentation for simple test validation script (75e60ff)
- Enhanced logging, bypassing some preconditionals as warning to resume (d9bd34a)
- Added local unit test operations for general SNS topic management (46dfe5e)
- Topik operasyonları eklendi. (8a6ef19)
- Initial commit (2d60eed)

