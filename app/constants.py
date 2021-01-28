DATABASE_PATH = '/home/denis/data/database.db'
ACCESS_LOG_PATH = '/home/denis/logs/access.log'
ERROR_LOG_PATH = '/home/denis/logs/error.log'
PIDFILE_PATH = '/home/denis/runtime.pid'

TOKEN_SIZE = 64

# Gunicorn

daemon = True
pidfile = PIDFILE_PATH
errorlog = ERROR_LOG_PATH
accesslog = ACCESS_LOG_PATH
