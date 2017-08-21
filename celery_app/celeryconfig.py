from celery.schedules import crontab
from datetime import timedelta
from kombu import Queue
from kombu import Exchange

result_serializer = 'json'

broker_url = "redis://q.213.name"
# broker_url = "amqp://q.213.name"
result_backend = "mongodb://q.213.name/celery"
# result_backend = "mongodb://s.213.name:12345/celery"
# result_backend = "redis://q.213.name"
timezone = "Asia/Shanghai"
imports = (
    'celery_app.task1',
    'celery_app.task2'
)

beat_schedule = {
    'add-every-20-seconds': {
        'task': 'celery_app.task1.multiply',
        'schedule': timedelta(seconds=20),
        'args': (5, 7)
    },
    'add-every-10-seconds': {
        'task': 'celery_app.task2.add',
        # 'schedule': crontab(hour=9, minute=10)
        'schedule': timedelta(seconds=10),
        'args': (23, 54)
    }
}

# task_queues = (
#     Queue('priority_high', exchange=Exchange('priority', type='direct'), routing_key='priority_high'),
#     Queue('priority_low', exchange=Exchange('priority', type='direct'), routing_key='priority_low'),
# )
#
# task_routes = ([
#     ('task1.multiply', {'queue': 'priority_high'}),
#     ('task2.add', {'queue': 'priority_low'})
# ],)

# 每分钟最大速率
# task_annotations = {
#     'task2.multiply': {'rate_limit': '10/m'}
# }
