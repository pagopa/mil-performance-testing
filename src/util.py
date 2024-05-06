import base64
import json
import os


def load_credentials():
    credentials_base64 = os.environ.get('CLIENT_CREDENTIALS_BASE64')
    client_credentials = base64.b64decode(credentials_base64).decode('utf-8')
    return json.loads(client_credentials)
