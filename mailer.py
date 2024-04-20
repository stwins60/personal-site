from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
import re


load_dotenv()

# sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
def ValidateEmail(email):
    regrex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    email_domain = ['gmail', 'yahoo', 'hotmail', 'outlook']
    user_email_domain = email.split('@')[1]
    user_email_domain = user_email_domain.split('.')[0]
    
    if re.fullmatch(regrex, email) and user_email_domain in email_domain:
        return True
    else:
        return False
def sendMyEmail(sender, recipient, subject, fname, lname, email, content):
    # """
    # Takes in email details to send an email to whoever.
    # """
    # message = f"""Message from {fname} {lname}: \n\n{content} \n\n
    # Email: {email}
    # """
    html_content = f"""
    <p>Hello {recipient},</p>
    <p>This form was submitted on your website by {fname} {lname}.</p>
    <p>Their message is as follows:</p>
    <p>{content}</p>
    <p>For further contact, their email is {email}</p>
    """


    # Sendgrid client
    email = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        html_content=html_content
    )
    
    # Sending the email 
    response = sg.send(email)
    
    # Returning either a successful message or not
    if response.status_code==202:
        return "Email has been accepted!"
    
    return "Email wasn't sent"

