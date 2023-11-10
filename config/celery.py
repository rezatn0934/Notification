from celery import Celery
from config.config import settings

app = Celery(__name__, include=['services.celery_services'])
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
