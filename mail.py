import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
EMAIL_HOST = 'mail.keywordlit.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'donotreply@keywordlit.com'
EMAIL_HOST_PASSWORD = 'keywordlit'
from_email = 'donotreply@keywordlit.com'
subject = 'This is a test email sent from Python.'
recipient_list = "rikenkhadela777@gmail.com"

# Email body
body = 'This is a test email sent from Python.'
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = recipient_list
msg['Subject'] = subject

# Attach the email body
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
server.sendmail(from_email, recipient_list, msg.as_string())
server.quit()

print("Email sent successfully")
