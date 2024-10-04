from dotenv import load_dotenv
from pydantic import EmailStr
from jinja2 import Template
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME="16f7b6f0d7151f",
    MAIL_PASSWORD="cd2bd08a6121c9",
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
