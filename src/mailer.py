import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
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
            
    def send_email(self, summary: dict, file_path: str): 
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = self.to_email
        msg['Subject'] = f'Relatório de Faturamento - {os.path.basename(file_path)}'
        
        html = f"""
        <html>
          <body>
            <h2>Resumo do Faturamento</h2>
            <p>Olá, segue o resumo do processamento:</p>
            <ul>
                <li><b>Total de Cobranças:</b> {summary['Total de Cobranças (Interno)']}</li>
                <li><b>Total de Cobranças:</b> {summary['Total de Cobranças (CSV)']}</li>
                <li><b>Valor Líquido:</b> R$ {summary['Valor Líquido Total (CSV)']:,.2f}</li>
                <li><b>Glosas Identificadas:</b> R$ {summary['Total de Glosas']:,.2f}</li>
                <li><b>Laudos Renomeados com Sucesso:</b> {summary['Laudos Renomeados com Sucesso']} itens precisam de atenção.</li>
            </ul>
            <p>O relatório detalhado está em anexo.</p>
          </body>
        </html> 
        """
        msg.attach(MIMEText(html, 'html'))
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(file_path)}",
        )
        msg.attach(part)
        
      
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls() 
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()

        except Exception as e:
            print(f"Erro ao conectar ao servidor SMTP: {e}")
        