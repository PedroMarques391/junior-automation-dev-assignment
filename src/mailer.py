import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

class Mailer:
    def __init__(self):
        self.smtp_server = os.getenv("MAIL_HOST")
        self.smtp_port = int(os.getenv("MAIL_PORT", 587))
        self.user = os.getenv("USER_EMAIL")
        self.password = os.getenv("USER_PASS")
        self.to_email = os.getenv("ADDRESSEE")
        
    def _init_server(self):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.user, self.password)

        return server

    def send_email(self, file_path: str, summary: dict):
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = self.to_email
        msg['Subject'] = f'Relatório de Faturamento - {os.path.basename(file_path)}'
        msg.attach(MIMEText("message", 'plain'))
        
        self._init_server().sendmail(self.user, self.to_email, msg.as_string())
        self._init_server().quit()
   