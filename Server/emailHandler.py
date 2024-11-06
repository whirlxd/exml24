import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USERNAME  = "brawlingbandits@gmail.com"
SMTP_PASSWORD = "nmjm kooe lsir eumj"
EMAIL_FROM = "brawlingbandits@gmail.com"


def sendEmail(token,email):
    try:
        server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT,)
        server.starttls()
        server.login(SMTP_USERNAME,SMTP_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = email
        msg['Subject'] = "EXML token"

        body = f'Your token is: {token}, Input your token in site to check your position in queue'
        msg.attach(MIMEText(body,'plain'))

        text = msg.as_string()
    
        server.sendmail(EMAIL_FROM,email,text)
        server.quit()
    except smtplib.SMTPException as e:

       return "invalid email"
