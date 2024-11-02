import requests
import json
from django.conf import settings
import re
from django.core.mail import send_mail
from .constants import WELCOME_EMAIL_MESSAGE, WELCOME_EMAIL_SUBJECT
def send_welcome_email(to_email, username):
    subject = WELCOME_EMAIL_SUBJECT
    message = WELCOME_EMAIL_MESSAGE.format(username=username, email_id=to_email)
    sender = settings.DEFAULT_FROM_EMAIL
    # Send the email
    send_mail(
        subject,
        message,
        sender, 
        [to_email], 
        fail_silently=False
    )