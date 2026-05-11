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
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 0;">
        <div style="background-color: #003399; padding: 20px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 24px;">Resumo do Faturamento</h1>
        </div>
        
        <div style="padding: 30px; border: 1px solid #ddd; border-top: none; max-width: 600px; margin: 0 auto;">
        <p style="font-size: 16px;">Olá, segue o resumo do processamento: </p>
        
        <div style="background-color: #f9f9f9; border-left: 5px solid #f27405; padding: 15px; margin: 20px 0;">
            <h3 style="color: #003399; margin-top: 0;">Métricas Consolidadas</h3>
            <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #eee;"><b>Total Interno:</b></td>
                <td style="text-align: right; padding: 8px 0; border-bottom: 1px solid #eee;">{int(summary['Total de Cobranças (Interno)'])}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #eee;"><b>Total Convênio (CSV):</b></td>
                <td style="text-align: right; padding: 8px 0; border-bottom: 1px solid #eee;">{int(summary['Total de Cobranças (CSV)'])}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #eee;"><b>Valor Líquido:</b></td>
                <td style="text-align: right; padding: 8px 0; border-bottom: 1px solid #eee; color: #28a745; font-weight: bold;">R$ {summary['Valor Líquido Total (CSV)']:,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #eee;"><b>Glosas Identificadas:</b></td>
                <td style="text-align: right; padding: 8px 0; border-bottom: 1px solid #eee; color: #dc3545;">R$ {summary['Total de Glosas']:,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0;"><b>Laudos Renomeados:</b></td>
                <td style="text-align: right; padding: 8px 0;">{int(summary['Laudos Renomeados com Sucesso'])} arquivos</td>
            </tr>
            </table>
        </div>
        <div>
        <p style="font-size: 14px; color: #666;">
            <b>Deixo em anexo o relatório detalhado.</b>
        </p>
        </div>
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
        