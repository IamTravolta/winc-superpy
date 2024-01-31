import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration (replace with your own values)
SMTP_SERVER = 'your_smtp_server'
SMTP_PORT = 587
SMTP_USERNAME = 'your_username'
SMTP_PASSWORD = 'your_password'
SENDER_EMAIL = 'your_email@example.com'
RECIPIENT_EMAIL = 'recipient@example.com'

def send_email(subject, body):
    """
    Send an email.

    Parameters:
    - subject (str): The subject of the email.
    - body (str): The body of the email.

    Returns:
    None
    """
    try:
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECIPIENT_EMAIL
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
    except Exception as e:
        print(f"Error sending email: {str(e)}")
