import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders, message_from_bytes
import ssl
import imaplib

class Mailing:
    def __init__(self, username, password):
        self.context = ssl.create_default_context()
        self.user = username
        self.password = password
        self.message = None
        self.imap_url = "imap.gmail.com"
        self.messages = []

    def create_message(self, user_to, subject, body):
        self.message = MIMEMultipart()
        self.message['From'] = self.user
        self.message['To'] = user_to
        self.message['Subject'] = subject
        self.message.attach(MIMEText(body, 'plain'))

    def send_email(self):
        """
        Outputs a BOOL True for Successful Email, False for Unsuccessful Email
        """
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = self.context) as server:
                server.login(self.user, self.password)
                server.sendmail(self.user, self.message["To"], self.message.as_string())
            return True
        except:
            return False

    def attach_file(self):
        # Attach a file (optional)
        filename = "example.txt"
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        self.message.attach(part)
    
    def try_login(self):
        """
        BOOL True: Success False: Unsuccessful
        """
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = self.context) as server:
                server.login(self.user, self.password)
            return True
        except:
            return False

    def get_emails(self):
        """
        Gets the last 5 emails sent to the User Email Address adn save them to class
        """
        try:
            self.messages = []
            connection = imaplib.IMAP4_SSL(self.imap_url)
            connection.login(self.user, self.password)
            connection.select("Inbox")
            type, data = connection.search(None, "ALL")
            mail_id = data[0]
            mail_id_list = mail_id.split()
            if len(mail_id_list) < 5:
                stop_index = len(mail_id_list)
            else:
                stop_index = 5

            for i in range(int(mail_id_list[-1]), int(mail_id_list[-stop_index]) - 1, -1):
                typ, data = connection.fetch(str(i),'(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = message_from_bytes(response_part[1])
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                self.messages.append({"from" : msg['from'], "subj" : msg['subject'], "body" : part.get_payload()})   
            self.messages_length = len(self.messages)
            return True
        except:
            return False