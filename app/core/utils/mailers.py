import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

load_dotenv()

HOST_URL = os.getenv("HOST_URL", "http://localhost:8000")

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("APP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

def read_html_file(file_path):
    """
    Read HTML file and return content.
    
    Args:
    file_path (str) : Path to HTML file.
    
    Returns:
    str : HTML content.
    """
    with open(file_path, 'r') as file:
        return file.read()
    
def render_template(template_name, context):
    """
    Render Jinja2 template.

    Args:
    template_name (str) : Name of the template.
    context (dict) : Context to render the template.
    """

    env = Environment(loader=FileSystemLoader('app/mailer'))
    template = env.get_template(template_name)
    return template.render(context)
    
def send_email(recipient_email, subject, html_content):
    """
    Send email via SMTP.
    
    Args:
    recipient_email (str) : Recipient email.
    subject (str) : Subject of email.
    html_content (str) : HTML content
    """

    if html_content:
        message = MIMEText(html_content, 'html')
    else:
        message = MIMEText(subject, 'plain')
    

    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(SENDER_EMAIL, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        server.close()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")


def send_login_email(recipient_email):
    """
    Send email that the user is logged in via SMTP.

    Args:
    recipient_email (str) : Recipient email.
    """
    html_content = read_html_file("app/mailer/signin.html")
    send_email(recipient_email, "You are signed in to Elencho!", html_content)
    
def send_update_pwd_email(recipient_email):
    """
    Send email that the user updated password via SMTP.
    
    Args:
    recipient_email (str) : Recipient email.
    """
    html_content = read_html_file("app/mailer/change_pwd.html")
    send_email(recipient_email, "Password Reset Detected!", html_content)

def send_invite_email(recipient_email, invite_id):
    """
    Send email that the user is invited to join the organization via SMTP.
    
    Args:
    recipient_email (str) : Recipient email.
    invite_id (int) : Invite ID.
    """
    context = {
        "invite_link": f"{HOST_URL}/invitations/accept?invite_id={invite_id}",
        "reject_link": f"{HOST_URL}/invitations/cancel?invite_id={invite_id}"
    }
    html_content = render_template("invite.html", context)

    send_email(recipient_email, "You are invited to join Elencho!", html_content)
    