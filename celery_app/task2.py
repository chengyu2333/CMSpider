import time
from celery_app import app


@app.task
def add(x, y):
    print(add)
    time.sleep(2)
    return x + y