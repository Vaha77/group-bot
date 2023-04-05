from data.config import DB_HOST, DB_PASS, DB_USER, DB_NAME, DB_PORT
from peewee import *

db = PostgresqlDatabase(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    telegram_id=BigIntegerField(primary_key=True)
    full_name=CharField(max_length=500)
    username=CharField(max_length=300, null=True)
    join_date=DateTimeField(formats=["%Y-%m-%d %H:%M:%S"])

    class Meta:
        db_name="Users"

class Channels(BaseModel):
    channel_id=BigIntegerField(primary_key=True)
    title=CharField(max_length=500)

    class Meta:
        db_name="Channels"

class Admins(BaseModel):
    admin_id=BigIntegerField(primary_key=True)
    admin_name=CharField(max_length=250)

    class Meta:
        db_name="Admins"


