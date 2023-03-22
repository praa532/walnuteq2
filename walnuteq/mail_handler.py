
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from walnuteq import settings


def mail_hanlders(instance,password1,email1,created=None):
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = email1

    message = MIMEMultipart()

    message["From"] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "sending mail for login" if created else "updated_password"
    dic = {"first_name": [instance.first_name], "last_name": [instance.last_name]}
    if created:
        df = pd.DataFrame(dic)
        file_name = f"{instance.id}.csv"
        df.to_csv(file_name)
        attachment = open(file_name, 'rb')

        obj = MIMEBase('application', 'octet-stream')

        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header('Content-Disposition', "attachment; filename= " + file_name)
        message.attach(MIMEText(
            f"user_name: {instance.email}" + " " + f"password: {password1}" + "\n" + f"login url: {settings.LOGIN_URL}"))
        message.attach(obj)
    else:
        message.attach(MIMEText(
            f"updated_password: {password1}" + "\n" + f"login url: {settings.LOGIN_URL}"))
    my_message = message.as_string()
    email_session = smtplib.SMTP(settings.EAMIL_HOST, settings.EMAIL_PORT)
    email_session.starttls()
    email_session.login(sender_email, password)
    email_session.sendmail(sender_email, receiver_email, my_message)
    email_session.quit()
    print("YOUR MAIL HAS BEEN SENT SUCCESSFULLY")
    return True
