from celery import Celery

app = Celery('math_tasks')


@app.task(bind=True)
def calculate_rating_task(self, force=False):
    pass


@app.task(bind=True)
def change_permission_task(self):
    pass
