import json

from constants import SECRETS_PATH


with open(SECRETS_PATH) as secrets_file:
    secrets = json.loads(secrets_file.read())
