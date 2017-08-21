import time
from celery_app import app


# class CallBack(Task):
#     def on_success(self, retval, task_id, args, kwargs):
#         print("----%s is done" % task_id)
#
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         pass


@app.task
def multiply(x, y):
    print("multiply")
    time.sleep(4)
    return x * y