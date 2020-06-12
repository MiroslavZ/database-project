from peewee import *

dbhandle = SqliteDatabase('..//petclinic.db')

#когда модели разнесены по файлам не получается правильно создать БД

class BaseModel(Model):
    class Meta:
        database = dbhandle


class Client(BaseModel):
    class Meta:
        database = dbhandle
        table_name = "clients"
    fio = TextField(null=False)
    email = TextField(null=False)
    phone = TextField(null=False)
    cat = TextField(null=True)
    password = TextField(null=False)


class Cat(BaseModel):
    class Meta:
        database = dbhandle
        table_name = "cats"

    name = TextField()
    owner_fio = ForeignKeyField(Client)
    age = IntegerField()
    cat_breed = TextField()


class Doctor(BaseModel):
    class Meta:
        database = dbhandle
        table_name = "doctors"
    fio = TextField(null=False)
    email = TextField(null=False)
    phone = TextField(null=False)
    password = TextField(null=False)
    work_time = BlobField()
    is_chief = BooleanField(null=False)


class Medication(BaseModel):
    class Meta:
        database = dbhandle
        table_name = "medications"
    title = TextField()
    description = TextField()
    cost = IntegerField(null=False)


class Appointment(BaseModel):
    class Meta:
        database = dbhandle
        table_name = "appointments"
    time = DateTimeField()
    doctor = ForeignKeyField(Doctor)
    cat = ForeignKeyField(Cat)
    state = TextField()
    cat_weight = DoubleField()
    need_med = ForeignKeyField(Medication)


def init_db():
    dbhandle.drop_tables([Cat, Client, Doctor, Medication, Appointment], safe=True)
    dbhandle.create_tables([Cat, Client, Doctor, Medication, Appointment], safe=True)
    return dbhandle


if __name__ == '__main__':
    init_db()