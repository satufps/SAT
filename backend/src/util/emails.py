import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from util import environment

def sendEmail(to, message, subject):
    coding = "UTF-8"
    msg = MIMEMultipart()
    msg["From"] = f'Sistema de alertas tempranas <{to}>'
    msg["To"] = to
    msg["Subject"] = Header(subject, coding)
    msg.attach(MIMEText(message, "plain"))
    email = environment.GMAIL_EMAIL
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, environment.GMAIL_PASSWORD)
    server.sendmail(email, to, msg.as_string())
    server.quit()
    print("Correo enviado") 
    
def sendMultipleEmail(recipients, message, subject ):
    coding = "UTF-8"
    msg = MIMEMultipart()
    msg["From"] = f'Sistema de alertas tempranas <noreply>'
    msg['To'] = ", ".join(recipients)
    msg["Subject"] = Header(subject, coding)
    msg.attach(MIMEText(message, "plain"))
    email = environment.GMAIL_EMAIL
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, environment.GMAIL_PASSWORD)
    server.sendmail(email, recipients, msg.as_string())
    server.quit()
    print("Correos enviados")