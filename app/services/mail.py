import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from jinja2 import Template

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM="mail@example.com",
    MAIL_PORT=2525,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True
)

async def send_registration_email(fullname: str, email: EmailStr):
    with open("app/templates/mail.html") as f:
        template_content = f.read()

    template = Template(template_content)
    rendered_html = template.render(fullname=fullname)

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=[email],
        body=rendered_html,  
        subtype="html" 
    )

    fm = FastMail(conf)
    await fm.send_message(message)
