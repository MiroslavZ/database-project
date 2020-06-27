import ORM.models2
from Petclinic.AppointmentClass import AppointmentClass
from Petclinic.DoctorClass import DoctorClass
from Petclinic.MedicationClass import MedicationClass
from Petclinic.CatClass import CatClass
from Petclinic.ClientClass import ClientClass
from Petclinic.PetclinicExeptions import ChangeAtributeException


class Database:
    _db = None
    _cursor = None

    def __init__(self):
        self._db = ORM.models2.conn
        self._cursor = ORM.models2.cursor

    @staticmethod
    def recreate_tables():
        ORM.models2.drop_all_tables()
        ORM.models2.create_tables()

    def add_doctor(self, fio: str, email: str, phone: str,
                   password: str, work_time, is_chief: bool):
        query = "Insert Into doctors (fio, email, phone, password, work_time, is_chief)" \
                "Values (?, ?, ?, ?, ?, ?)"
        self._cursor.execute(query, [fio, email, phone, password, work_time, is_chief.__str__()])
        self._db.commit()

    def add_medication(self, title: str, description: str, cost):
        query = "Insert Into medications (title, description, cost)" \
                "Values (?, ?, ?)"
        self._cursor.execute(query, [title, description, cost])
        self._db.commit()

    def add_cat(self, name: str, owner_id: int, age: int, cat_breed: str):
        query = "Insert Into cats (name, owner_id, age, cat_breed)" \
                "Values (?, ?, ?, ?)"
        self._cursor.execute(query, [name, owner_id, age, cat_breed])
        self._db.commit()

    def add_client(self, fio: str, email: str, phone: str, cat, password: str):
        query = "Insert Into clients (fio, email, phone, cat, password)" \
                "Values (?, ?, ?, ?, ?)"
        self._cursor.execute(query, [fio, email, phone, cat, password])
        self._db.commit()

    def add_appointment(self, time: str, doctor_id: int, cat_id: int, state: str, need_med):
        query = "Insert Into appointments (time, doctor_id, cat_id, state, need_med)" \
                "Values (?, ?, ?, ?, ?)"
        self._cursor.execute(query, [time, doctor_id, cat_id, state, need_med])
        self._db.commit()

    def change_medication_cost(self, id_med: int, cost: float):
        if cost > 0:
            query = 'Update medications Set cost = ' + str(cost) + ' Where id = ' + "'" + str(id_med) + "'"
            self._cursor.execute(query)
            self._db.commit()
        else:
            raise ChangeAtributeException

    def change_doctor_status(self, id_doc: int, status: bool):
        query = 'Update doctors Set is_chief = ' + "'" + str(status) + "'" + ' Where id = ' + "'" + \
                str(id_doc) + "'"
        self._cursor.execute(query)
        self._db.commit()

    def change_cat(self, id_cat: int, name: str, age: int, cat_breed: str):
        query = f"Update cats Set name = '{name}', age = " \
                f"'{age.__str__()}', cat_breed = '{cat_breed}' " \
                f"Where id = '{str(id_cat)}'"
        self._cursor.execute(query)
        self._db.commit()

    def change_doctor(self, id_doc: int, fio: str, email: str, phone: str,
                  password: str, work_time, is_chief: bool):
        query = f"Update doctors Set fio = '{fio}', email = " \
                f"'{email}', phone = '{phone}', " \
                f"password = '{password}', work_time = '{work_time}', " \
                f"is_chief = '{is_chief.__str__()}' " \
                f"Where id = '{str(id_doc)}'"
        self._cursor.execute(query)
        self._db.commit()

    def change_doctor_without_password(self, id_doc: int, fio: str, email: str, phone: str,
                  work_time, is_chief: bool):
        query = f"Update doctors Set fio = '{fio}', email = " \
                f"'{email}', phone = '{phone}', " \
                f"work_time = '{work_time}', " \
                f"is_chief = '{is_chief.__str__()}' " \
                f"Where id = '{str(id_doc)}'"
        self._cursor.execute(query)
        self._db.commit()

    def change_client(self, id_client: int, fio: str, email: str, phone: str,
                      password: str):
        query = f"Update clients Set fio = '{fio}', email = " \
                f"'{email}', phone = '{phone}', " \
                f"password = '{password}' " \
                f"Where id = '{str(id_client)}'"
        self._cursor.execute(query)
        self._db.commit()

    def change_medication(self, id_med: int, title: str,
                          description: str, cost: str):
        query = f"Update medications Set title = '{title}', description = " \
                f"'{description}', cost = '{cost}' " \
                f"Where id = '{str(id_med)}'"
        self._cursor.execute(query)
        self._db.commit()

    def get_my_pets(self, id_client: int) -> dict:
        self._cursor.execute("Select * From cats Where owner_id = " + str(id_client))
        cats_dict = {}
        for row in self._cursor.fetchall():
            cat = CatClass(row[0], row[1], row[2], row[3], row[4])
            cats_dict[cat.id] = cat.__str__()
        return cats_dict

    def get_my_pet(self, id_client: int, cat_name) -> str:
        self._cursor.execute(f"Select * From cats Where owner_id = {str(id_client)} AND name = {cat_name}")
        fetch = self._cursor.fetchone()
        cat = CatClass(fetch[0], fetch[1], fetch[2], fetch[3], fetch[4])
        return cat.__str__()

    def get_all_cats(self) -> dict:
        self._cursor.execute("Select * From cats")
        cats_dict = {}
        for row in self._cursor.fetchall():
            cat = CatClass(row[0], row[1], row[2], row[3], row[4])
            cats_dict[cat.id] = cat.__str__()
        return cats_dict

    def get_all_doctors(self) -> dict:
        self._cursor.execute("Select * From doctors")
        doctors_dict = {}
        for row in self._cursor.fetchall():
            is_chief = row[6] == "True"
            doc = DoctorClass(row[0], row[1], row[2], row[3], row[4], row[5], is_chief)
            doctors_dict[doc.id] = doc.__str__()
        return doctors_dict

    def get_all_appointments(self) -> dict:
        self._cursor.execute("Select * From appointments")
        app_dict = {}
        for row in self._cursor.fetchall():
            app = AppointmentClass(row[0], row[1], row[2], row[3], row[4], row[5])
            app_dict[app.id] = app.__str__()
        return app_dict

    def get_all_medications(self) -> dict:
        self._cursor.execute("Select * From medications")
        medications_dict = {}
        for row in self._cursor.fetchall():
            medication = MedicationClass(row[0], row[1], row[2], row[3])
            medications_dict[medication.id] = medication.__str__()
        return medications_dict

    def get_all_clients(self) -> dict:
        self._cursor.execute("Select * From clients")
        clients_dict = {}
        for row in self._cursor.fetchall():
            client = ClientClass(row[0], row[1], row[2], row[3], row[4], row[5])
            clients_dict[client.id] = client.__str__()
        return clients_dict

    def delete_doctor(self, id_doc: int):
        query = 'Delete From doctors Where id = ' + "'" + str(id_doc) + "'"
        self._cursor.execute(query)
        self._db.commit()

    def doctor_by_fio(self, fio: str):
        query = 'Delete From doctors Where fio = ' + "'" + fio + "'"
        self._cursor.execute(query)
        self._db.commit()

    def delete_cat(self, id_cat: int):
        query = 'Delete From cats Where id = ' + "'" + str(id_cat) + "'"
        self._cursor.execute(query)
        self._db.commit()

    def delete_client(self, id_client: int):
        query = 'Delete From clients Where id = ' + "'" + str(id_client) + "'"
        self._cursor.execute(query)
        self._db.commit()

    def delete_medication(self, id_med: int):
        query = 'Delete From medications Where id = ' + "'" + str(id_med) + "'"
        self._cursor.execute(query)
        self._db.commit()

    def delete_appointment(self, id_app: int):
        query = 'Delete From appointments Where id = ' + "'" + str(id_app) + "'"
        self._cursor.execute(query)
        self._db.commit()

    def is_doctor_with_email(self, email: str) -> bool:
        try:
            self._cursor.execute(f"Select * From doctors where email = \"{email}\"")
            return self._cursor.fetchone() is not None
        except:
            return False

    def is_client_with_email(self, email: str) -> bool:
        try:
            self._cursor.execute(f"Select * From clients where email = \"{email}\"")
            return self._cursor.fetchone() is not None
        except:
            return False

    def get_doctor_by_email(self, email: str) -> str:
        # self._cursor.execute("Select * From doctors where email = " + email)
        self._cursor.execute(f'Select * From doctors WHERE email = \"{email}\"')
        fetch = self._cursor.fetchone()
        is_chief = fetch[6] == "True"
        doctor = DoctorClass(fetch[0], fetch[1], fetch[2], fetch[3], fetch[4], fetch[5], is_chief).__str__()
        return doctor

    def get_client_by_email(self, email: str) -> str:
        self._cursor.execute(f'Select * From clients WHERE email = \"{email}\"')
        fetchone = self._cursor.fetchone()
        client = ClientClass(fetchone[0], fetchone[1], fetchone[2], fetchone[3], fetchone[4], fetchone[5]).__str__()
        return client

    def get_doctor_by_fio(self, doctor_name: str) -> str:
        self._cursor.execute(f'Select * From doctors WHERE fio = \"{doctor_name}\"')
        fetchone = self._cursor.fetchone()
        is_chief = fetchone[6] == 'True'
        doctor = DoctorClass(fetchone[0], fetchone[1], fetchone[2], fetchone[3],
                             fetchone[4], fetchone[5], is_chief).__str__()
        return doctor
