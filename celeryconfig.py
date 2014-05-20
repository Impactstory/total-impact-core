import os
import sys
import urlparse
from kombu import Exchange, Queue

sys.path.append('.')

## Broker settings.
# BROKER_URL = os.getenv("CLOUDAMQP_URL", "amqp://guest@localhost//")
# CELERY_RESULT_BACKEND = "amqp"


redis_url = os.environ.get('REDIS_URL')
if not redis_url.endswith("/"):
    redis_url += "/"

BROKER_URL = redis_url + "0"
CELERY_RESULT_BACKEND = redis_url + "0"
REDIS_CONNECT_RETRY = True


# these options will be defaults in future as per http://celery.readthedocs.org/en/latest/getting-started/brokers/redis.html
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
BROKER_TRANSPORT_OPTIONS = {'fanout_patterns': True}

CELERY_DEFAULT_QUEUE = 'core_main'
CELERY_QUEUES = (
    Queue('core_main', Exchange('core_main'), routing_key='core_main'),
)


CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_ENABLE_UTC=True
CELERY_TASK_RESULT_EXPIRES = 60*60  # 1 hour

# List of modules to import when celery starts.
CELERY_IMPORTS = ("tasks",)

CELERY_ANNOTATIONS = {
    'celery.chord_unlock': {'soft_time_limit': 60*5},  # five minutes
}