from fastapi import (BackgroundTasks, UploadFile, File, Depends, HTTPException, status)
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List
from models import User
from dotenv import dotenv_values
import jwt

config_credentials = dotenv_values(".env")


conf = ConnectionConfig(
    MAIL_USERNAME= config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASSWORD"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS= True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS= True
)

class EmailSchema(BaseModel):
    email: List[EmailStr]

async def send_email(email: EmailSchema, instance: User):
    token_data = {
        "id" : instance.id,
        "username": instance.username
    }

    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm="HS256")

    template = f"""
    <!DOCTYPE html>
    <html>
      <head>
      </head>
      <body>
        <div style="display: flex; align-items: center; justify-content: center; flex-direction: column">
           <h3>Account Verification</h3>
           <br>
           <p>Thanks for choosing EasyShop, please click on the button below
           to verify your account:</p>
            <a href="http://127.0.0.1:8000/verification/?token={token}" 
              style="margin-top: 1rem; padding: 1rem; background-color: #0275d8; color: white; 
              text-decoration: none; border-radius: 0.5rem; font-size: 1rem">
              Verify your email
            </a>
            <p>Please kindly ignore this email if you did not register for EasyShopas and nothiong will happend. Thanks</p>
        </div>
      </body>
    </html>
    """

    message = MessageSchema(
        subject = "EasyShopas Account Verification Email",
        recipients= email, #LIST OF RECIPIENTS
        body= template,
        subtype = "html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)