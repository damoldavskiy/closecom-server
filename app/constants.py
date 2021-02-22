DATABASE_PATH = '/home/denis/data/database.db'
ACCESS_LOG_PATH = '/home/denis/logs/access.log'
ERROR_LOG_PATH = '/home/denis/logs/error.log'
PIDFILE_PATH = '/home/denis/runtime.pid'
SECRETS_PATH = '/home/denis/data/secrets.json'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465

TOKEN_SIZE = 32
MIN_PASSWORD_LENGTH = 4

# Gunicorn

daemon = True
pidfile = PIDFILE_PATH
errorlog = ERROR_LOG_PATH
accesslog = ACCESS_LOG_PATH
