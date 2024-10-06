import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def initialize_server():
    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    return server

def setLoginCredentials(user_email, app_password, report_sending_email):
    global senderId, appPassword, receiverId, server
    senderId = user_email
    appPassword = app_password
    receiverId = report_sending_email
    server = initialize_server()
    server.login(senderId, appPassword)

def setEmail(content):
    sender = senderId
    receiver = receiverId
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = "Your email recap"
    
    message.attach(MIMEText(content, 'html'))
    try:
        server.sendmail(sender, receiver, message.as_string())
        print("Sent email to the given address")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
    finally:
        server.quit()
