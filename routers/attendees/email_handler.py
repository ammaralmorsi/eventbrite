import os

from enum import Enum

from fastapi import HTTPException
from fastapi import status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from datetime import timedelta

from dependencies.models.attendees import Attendee
from dependencies.db.events import EventDriver
event_driver=EventDriver()

class EmailHandler:
    def __init__(self):
        self.source_email = os.environ.get("EVENTBRITE_EMAIL")
        self.source_password = os.environ.get("EVENTBRITE_PASSWORD")
        self.message = None
        self.expiration_date = datetime.utcnow() + timedelta(hours=24)

    def send_email(self, email: str,event_id:str,attendee:Attendee):
        self.message = MIMEMultipart()
        self.message["From"] = self.source_email
        self.message["To"] = email
        self.message["Subject"] = "Order Confirmation"
        event=event_driver.get_event_by_id(event_id)
        #msg="Dear "+email+" ,\n"+"Thank you for your order for "+event["name"]+" event.\n"+"Your order is confirmed.\n"+"Your order id is "+event["id"]+"\n"+"Your order will expire at "+str(self.expiration_date)+"\n"+"Best Regards,\n"+"Eventbrite Team"
        msg="Dear "+attendee["first_name"]+" "+attendee["last_name"]+" ,\n"+"Thank you for your order for event "+event["basic_info"]+" event.\n"+"Your order is confirmed.\n"+"Your order id is "+attendee["order_id"]+"\n"+"Best Regards,\n"+"Eventbrite Team"
        self.message.attach(MIMEText(msg, "plain"))
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            # server.starttls()
            server.login(self.source_email, self.source_password)
            server.sendmail(self.source_email, email, self.message.as_string())
        except smtplib.SMTPRecipientsRefused:
            raise HTTPException(detail="recipient email refused.",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except smtplib.SMTPException:
            raise HTTPException(detail="failed to send email.",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except AttributeError:
            raise HTTPException(detail="no source email.",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#e=EmailHandler()
#e.send_email("ahmedfathy1234553@gmail.com","hbdshb")
