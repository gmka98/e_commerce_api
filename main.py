from fastapi import FastAPI, HTTPException, status
from starlette.responses import HTMLResponse
from starlette.requests import  Request 
from tortoise.signals import post_save
from typing import List, Optional, Type
from models import *
from authentication import (get_hashed_password, very_token)
from tortoise import BaseDBAsyncClient
from tortoise.contrib.fastapi import register_tortoise
from emails import *
from fastapi.templating import Jinja2Templates

app = FastAPI()

@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
    
    if created:
        business_obj = await Business.create(
            business_name=instance.username, owner=instance
        )
        # send the email
        await business_pydantic.from_tortoise_orm(business_obj)
        await send_email([instance.email], instance)


@app.post("/registration")
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True) 
    user_info["password"] = get_hashed_password(user_info["password"])
    user_object = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_object)
    return{
        "status" : "ok",
        "data" : f"Hello {new_user.username} thanks for choosing our services. Please check your email inbox to and click on the link to confirm your registration."
    }
templates = Jinja2Templates(directory="templates")
@app.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await very_token(token)

    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html", 
                                          {"request": request, "username" : user.username})
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid token or expire",
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.get("/")
def index():
    return{"Hello" : "World"}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
