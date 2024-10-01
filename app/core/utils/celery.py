from celery import Celery
from os import getenv
from dotenv import load_dotenv

DATABASE_URI = getenv('DATABASE_URI')

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0', 
    backend= DATABASE_URI)  

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
