import os

def create_project_structure():
    folders = [
        "src", 
        "tests", 
        "templates", 
        "config"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Folder '{folder}' created.")
    
    # Temel dosyalar
    files = {
        "src/topic_manager.py": "",
        "src/notification_manager.py": "",
        "src/config_manager.py": "",
        "src/cli.py": "",
        "tests/test_topic_manager.py": "",
        "tests/test_notification_manager.py": "",
        "tests/test_config_manager.py": "",
        "templates/reminder_template.md": "# Reminder Template",
        "templates/deletion_template.md": "# Deletion Template",
        "config/config.yaml": "reminder:\n  day_1: 2\n  day_2: 5\n  day_3: 7\ndelection:\n  day_3: 9\n",
        "README.md": "# Project Overview",
        "requirements.txt": "boto3\nJinja2\nPyYAML\n"
    }

    for file_path, content in files.items():
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_path}' created.")

if __name__ == "__main__":
    create_project_structure()


