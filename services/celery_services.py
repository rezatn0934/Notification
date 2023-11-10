import structlog
from pydantic import EmailStr
from celery import Task, shared_task
from custom_logger.logger import setup_logger
from services.send_mail_services import get_email_sender
import asyncio

setup_logger()
logger = structlog.get_logger("elastic_logger")


class MyTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True
    retry_jitter = False
    task_acks_late = True

    def retry(self, args=None, kwargs=None, exc=None, throw=True,
              eta=None, countdown=None, max_retries=None, **options):
        retry_count = self.request.retries
        retry_eta = eta or (countdown and f'countdown={countdown}') or 'default'
        event = f'CeleryTask.{self.name}',
        msg = {'correlation_id': args[-1],
               'task_name': self.name,
               'message': f'Retrying task {self.name} (retry {retry_count}) in {retry_eta} seconds',
               'task_id': self.request.id, 'args': args, 'kwargs': kwargs,
               'exception': str(exc), 'retry_count': retry_count,
               'max_retries': max_retries,
               'retry_eta': retry_eta}

        async def log_func():
            await logger.warning(event=event, **msg)

        asyncio.run(log_func())
        super().retry(args, kwargs, exc, throw, eta, countdown, max_retries, **options)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        event = f'CeleryTask.{self.name}',
        msg = {'correlation_id': args[-1],
               'task_name': self.name,
               'message': f'Task {self.name} failed: {str(exc)}',
               'task_id': self.request.id, 'args': args, 'kwargs': kwargs,
               'exception': str(exc), }

        async def log_func():
            await logger.error(event=event, **msg)

        asyncio.run(log_func())

    def on_success(self, retval, task_id, args, kwargs):
        event = f'CeleryTask.{self.name}',
        msg = {'correlation_id': args[-1],
               'task_name': self.name,
               'message': f'Task {self.name} completed successfully',
               'task_id': self.request.id, 'args': args, 'kwargs': kwargs,
               'output_data': retval, }

        async def log_func():
            await logger.info(event=event, **msg)

        asyncio.run(log_func())


@shared_task(base=MyTask, task_time_limit=60, acks_late=True)
def send_mail_task(email: EmailStr, subject: str, message: str, correlation_id):
    email_sender = get_email_sender()
    email_sender.send_email(recipient_email=email, subject=subject, message_body=message)
