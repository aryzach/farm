import smtplib
import sys
import password 
import os
from datetime import datetime
 
#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'twistedfieldsdev@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = password.GMAIL_PASSWORD  #change this to match your gmail password

class Emailer:
    def sendmail(self, recipient, subject, content):
         
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
 
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
 
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
 
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit
 

#Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
def emailData():
    sender = Emailer()

    sendTo = 'zach_asmith@yahoo.com'
    emailSubject = subject 
    emailContent = content 

    sender.sendmail(sendTo, emailSubject, emailContent)  
