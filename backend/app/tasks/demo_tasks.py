from celery_app import celery
import time
# Test task
@celery.task
def addition(x, y):
    print("RUNNING. The output is ", x + y)
    time.sleep(15)
    return "DONE"