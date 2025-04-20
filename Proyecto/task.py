from celery import Celery
from flask_mail import Mail, Message
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.environ.get('CELERY_BROKER_URL'),
        backend=os.environ.get('CELERY_RESULT_BACKEND')
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = Flask(__name__)
flask_app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_USERNAME')
)

mail = Mail(flask_app)
celery = make_celery(flask_app)

@celery.task
def send_email(subject, recipient, body):
    msg = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(msg)
