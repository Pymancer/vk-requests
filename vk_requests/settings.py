# Test settings
import os
import json
import os.path

# Set your environment variables for testing or put values here or into a credentials file
creds_file = './creds.json'
creds = {"user_login": None, "user_password": None, "app_id": None, "phone_number": None}
if os.path.isfile(creds_file):
    with open(creds_file) as f:
        creds = json.loads(f.read())

# user email or phone number
USER_LOGIN = creds['user_login'] or os.getenv('VK_USER_LOGIN', '')
USER_PASSWORD = creds['user_password'] or os.getenv('VK_USER_PASSWORD', '')
# aka API/Client ID
APP_ID = creds['app_id'] or os.getenv('VK_APP_ID')
PHONE_NUMBER = creds['phone_number'] or os.getenv('VK_PHONE_NUMBER')
