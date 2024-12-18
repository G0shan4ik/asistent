from peewee import (
    TextField,
    BigIntegerField,
    Model,
    SqliteDatabase,
    ForeignKeyField,
    DateTimeField,
)

from pathlib import Path
from os import getcwd

path = Path(getcwd()).joinpath('assistant.db')
db = SqliteDatabase(path)
print(path)


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    unique_id = TextField(null=True, unique=True, primary_key=True)
    user_id = BigIntegerField(unique=False)


class CoursesCurrencies(BaseModel):
    dollar_ruble_by = BigIntegerField(null=True)
    dollar_ruble_ru = BigIntegerField(null=True)
    rouble_ru_by = BigIntegerField(null=True)

    update_time = DateTimeField(null=True)


class Job(BaseModel):
    user = ForeignKeyField(Users)
    name_job = TextField(null=True, unique=False)

class JobStatistics(BaseModel):
    job = ForeignKeyField(Job)
    date_of_payment = DateTimeField(null=True)
    amount_of_deposit = BigIntegerField(null=True)
    currency = TextField(null=True)


def init():
    Users.create_table(safe=True)
    CoursesCurrencies.create_table(safe=True)
    Job.create_table(safe=True)
    JobStatistics.create_table(safe=True)