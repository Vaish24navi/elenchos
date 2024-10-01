from apscheduler.schedulers.background import BackgroundScheduler
from app.core.utils.mailers.py import send_email
from datetime import datetime, timedelta

def schedule_email(recipient_email, subject, body, schedule_time):
    """
    Schedule an email to be sent at a later time.
    
    Args:
    recipient_email (str) : Recipient email.
    subject (str) : Subject of email.
    body (str) : Email body.
    schedule_time (datetime) : Time to send the email.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_email_invite.s(recipient_email, subject, body),
        'date',
        run_date=schedule_time
    )
    scheduler.start()
