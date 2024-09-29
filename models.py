from tortoise import Model,fields, 
from pydantic import BaseModel


class User(Model):
    id = fields.IntField(pk = True, index = True)
    username = fields.CharField(max_lenght=20, null = False, unique = True)
    email = fields. CharField(max_lenght=200, null = False, unique = True)
    password = fields.CharField(max_lenght=100, null = False)
    is_verified = fields.BooleanField(default = False)
    join_data = fields.DatetimeField(default = datetime.utcnow)


class Business(Model):
    id = fields.InterField(pk = True, index = True)
    Business_name = fields.CharField
    city = fields.CharField(max_)