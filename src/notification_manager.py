import smtplib
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

class NotificationManager:
    def __init__(self, config_manager):
        self.config = config_manager.load_config()
        self.env = Environment(loader=FileSystemLoader('templates'))

    def send_email(self, recipient, subject, body):
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = self.config['smtp']['from_email']
        msg['To'] = recipient

        with smtplib.SMTP(self.config['smtp']['host'], self.config['smtp']['port']) as server:
            server.send_message(msg)

    def generate_email(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)

    def send_reminder(self, topic_arn, days_passed):
        subject = f"Reminder: {topic_arn} has been inactive for {days_passed} days"
        body = self.generate_email('reminder_template.md', {
            'topic_name': topic_arn.split(':')[-1],
            'days_passed': days_passed,
            'delete_in_days': self.config['deletion']['day_3'] - days_passed
        })
        self.send_email(self.config['admin']['email'], subject, body)

    def send_deletion_notice(self, topic_arn):
        subject = f"Notice: {topic_arn} has been deleted"
        body = self.generate_email('deletion_template.md', {
            'topic_name': topic_arn.split(':')[-1],
            'total_days': self.config['deletion']['day_3']
        })
        self.send_email(self.config['admin']['email'], subject, body)

    def configure_notification_schedule(self, reminder_days, deletion_day):
        self.config['reminder']['day_1'] = reminder_days[0]
        self.config['reminder']['day_2'] = reminder_days[1]
        self.config['reminder']['day_3'] = reminder_days[2]
        self.config['deletion']['day_3'] = deletion_day
        self.save_config()

    def save_config(self):
        with open('config/config.yaml', 'w') as file:
            yaml.safe_dump(self.config, file)

