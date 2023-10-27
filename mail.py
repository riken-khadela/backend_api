import smtplib

sender = 'rikenkhadela777@gmail.com'
receivers = ['rikenkhadela85@gmail.com']
message = """From: From Person <from@example.com>
To: To Person <to@example.com>
Subject: SMTP email example


This is a test message.
"""

smtpObj = smtplib.SMTP('localhost')
smtpObj.sendmail(sender, receivers, message)         
print("Successfully sent email")