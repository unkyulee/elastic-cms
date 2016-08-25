import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(user, password, recipient, subject, body, content_type="plain"):
    gmail_user = user
    gmail_pwd = password

    # recipients
    recipients = recipient if type(recipient) is list else [recipient]

    # Prepare actual message
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = ", ".join(recipients)

    # format body as plain or html
    if content_type == "plain":
        text = MIMEText(body.encode('utf-8'), 'plain','utf-8')
    elif content_type == "html":
        text = MIMEText(body.encode('utf-8'), 'html','utf-8')

    # attach to the message
    msg.attach(text)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, recipients, msg.as_string())
        server.close()
        return True
    except:
        return False
