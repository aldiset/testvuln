from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

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
    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=[email],
        body=f"Hi {fullname},\n\nYou have successfully registered.\n\nThanks!",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
