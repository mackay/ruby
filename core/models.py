from peewee import SqliteDatabase
from peewee import Model
from peewee import TextField, CharField
from peewee import IntegerField, FloatField
from peewee import DateTimeField
from peewee import ForeignKeyField

from datetime import datetime
import json


#set sane default log levels
import logging
logging.getLogger('peewee').setLevel(logging.INFO)
logging.getLogger("peewee.pool").setLevel(logging.DEBUG)

database = SqliteDatabase('detector.db')


class JSONField(TextField):
    def db_value(self, value):
        if value is not None:
            return json.dumps(value)

        return None

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class BaseModel(Model):
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__( *args, **kwargs )
        self._meta.base_uri = self._meta.db_table

    class Meta:
        database = database
        base_uri = "unknown"


class OrdinalModel(BaseModel):
    ordinal = IntegerField(default=0)


class ClassModel(OrdinalModel):
    class_path = CharField(max_length=1024)
    context = JSONField(default="{}")


class SystemOption(BaseModel):
    key = CharField(max_length=64, unique=True, index=True)
    value = CharField(max_length=255)
    class Meta:
        database = database
        base_uri = "/option"


class Sequence(BaseModel):
    name = CharField(max_length=255)
    class Meta:
        database = database
        base_uri = "/sequence"


class Frame(OrdinalModel):
    sequence = ForeignKeyField(rel_model=Sequence, related_name="frames")
    duration_ms = IntegerField(default=1000*5)

    class Meta:
        database = database
        base_uri = "/frame"
        order_by = ['ordinal']


class FrameSprite(ClassModel):
    frame = ForeignKeyField(rel_model=Frame, related_name="sprites")

    class Meta:
        database = database
        base_uri = "/sprite"
        order_by = ['ordinal']


class FrameSpriteDynamic(ClassModel):
    sprite = ForeignKeyField(rel_model=FrameSprite, related_name="dynamics")

    class Meta:
        database = database
        base_uri = "/dynamic"
        order_by = ['ordinal']



def initialize():
    database.connect()

    database.create_tables([ SystemOption ], safe=True)
    database.create_tables([ Sequence ], safe=True)
    database.create_tables([ Frame ], safe=True)
    database.create_tables([ FrameSprite ], safe=True)
    database.create_tables([ FrameSpriteDynamic ], safe=True)

    database.close()
