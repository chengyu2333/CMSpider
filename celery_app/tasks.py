import time
from celery import Celery

# broker = "amqp://q.213.name"
broker = "redis://q.213.name"
backend = "mongodb://s.213.name:12345/celery"
app = Celery("my_task", broker=broker, backend=backend)
# app = Celery("my_task", broker=broker, backend="")

@app.task
def add(x, y):
    print("add")
    time.sleep(5)
    return x+y

# if __name__ == "__main__":
#     app.worker_main()


