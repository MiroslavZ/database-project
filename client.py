import requests
import json

from Petclinic.AppointmentClass import AppointmentClass
from Petclinic.CatClass import CatClass
from Petclinic.ClientClass import ClientClass
from Petclinic.DoctorClass import DoctorClass
from Petclinic.MedicationClass import MedicationClass

# пишешь свой ip ниже
server_address = "http://192.168.1.128"
session = requests.Session()


def get_all_doctors():
    session.headers['class'] = "doctor"
    doctors_encrypted = json.loads(session.get(server_address).text)
    doctors_decrypted = {}
    for key in doctors_encrypted:
        doc = DoctorClass.decrypt(doctors_encrypted[key])
        doctors_decrypted[doc.id] = doc
    return doctors_decrypted


def get_all_appointments():
    session.headers['class'] = "appointment"
    appointments_encrypted = json.loads(session.get(server_address).text)
    appointments_decrypted = {}
    for key in appointments_encrypted:
        doc = AppointmentClass.decrypt(appointments_encrypted[key])
        appointments_decrypted[doc.id] = doc
    return appointments_decrypted


def get_doctor_by_email(email: str) -> str:
    doctors = get_all_doctors()
    for key in doctors:
        if doctors[key].email == email:
            return doctors[key].__str__()
    return ''

def get_doctor_by_id(id_doc: int):
    doctors = get_all_doctors()
    for key in doctors:
        if doctors[key].id == id_doc:
            return doctors[key]
    return None

def get_client_by_email(email: str) -> str:
    session.headers['class'] = "get_client_by_email"
    session.headers['email'] = encrypted_string(email)
    return session.get(server_address).text

def get_client_class_by_email(email: str):
    clients = get_all_clients()
    for key in clients:
        if clients[key].email == email:
            return clients[key]
    return None


def get_client_by_fio(fio: str):
    clients = get_all_clients()
    for key in clients:
        if clients[key].fio == fio:
            return clients[key]
    return None

def is_doctor_with_email(email: str) -> bool:
    session.headers['class'] = "is_doctor_with_email"
    session.headers['email'] = encrypted_string(email)
    return session.get(server_address).text == 'True'


def is_client_with_email(email: str) -> bool:
    session.headers['class'] = "is_client_with_email"
    session.headers['email'] = encrypted_string(email)
    return session.get(server_address).text == 'True'


def get_all_cats():
    session.headers['class'] = "cat"
    cats_encrypted = json.loads(session.get(server_address).text)
    cats_decrypted = {}
    for key in cats_encrypted:
        cat = CatClass.decrypt(cats_encrypted[key])
        cats_decrypted[cat.id] = cat
    return cats_decrypted


def get_all_clients():
    session.headers['class'] = "client"
    clients_encrypted = json.loads(session.get(server_address).text)
    clients_decrypted = {}
    for key in clients_encrypted:
        client = ClientClass.decrypt(clients_encrypted[key])
        clients_decrypted[client.id] = client
    return clients_decrypted


def get_all_medications():
    session.headers['class'] = "medication"
    medication_encrypted = json.loads(session.get(server_address).text)
    medication_decrypted = {}
    for key in medication_encrypted:
        medication = MedicationClass.decrypt(medication_encrypted[key])
        medication_decrypted[medication.id] = medication
    return medication_decrypted

def get_med_by_title(title: str):
    meds = get_all_medications()
    for key in meds:
        if meds[key].title == title:
            return meds[key]
    return None

def get_my_pets(id_client: int):
    session.headers['class'] = 'my_pets'
    session.headers['id'] = id_client.__str__()
    cats_encrypted = json.loads(session.get(server_address).text)
    cats_decrypted = {}
    for key in cats_encrypted:
        cat = CatClass.decrypt(cats_encrypted[key])
        cats_decrypted[cat.id] = cat
    return cats_decrypted


def get_my_pet(id_client: int, cat_name: str):
    session.headers['class'] = 'my_pet'
    session.headers['id'] = id_client.__str__()
    session.headers['cat_name'] = encrypted_string(cat_name)
    cat_encrypted = session.get(server_address).text
    cat_decrypted = CatClass.decrypt(cat_encrypted)
    return cat_decrypted

def get_doctor_by_fio(fio_doctor: str):
    doctors = get_all_doctors()
    for key in doctors:
        if doctors[key].fio == fio_doctor:
            return doctors[key]
    return None


def add_doctor(fio: str, email: str, phone: str,
               password: str, work_time, is_chief: bool):
    session.headers['class'] = 'doctor'
    session.headers['fio'] = encrypted_string(fio)
    session.headers['email'] = encrypted_string(email)
    session.headers['phone'] = phone
    session.headers['password'] = password
    session.headers['work_time'] = work_time
    session.headers['is_chief'] = is_chief.__str__()
    session.post(server_address)


def add_cat(name: str, owner_id: int, age: int, cat_breed: str):
    session.headers['class'] = 'cat'
    session.headers['name'] = encrypted_string(name)
    # session.headers['name'] = name
    session.headers['owner_id'] = owner_id.__str__()
    session.headers['age'] = age.__str__()
    session.headers['cat_breed'] = encrypted_string(cat_breed)
    session.post(server_address)
    # session.post(server_address, data={'name': name.encode('utf-8')})


def add_client(fio: str, email: str, phone: str, cat_id: int, password: str):
    session.headers['class'] = 'client'
    session.headers['fio'] = encrypted_string(fio)
    session.headers['email'] = encrypted_string(email)
    session.headers['phone'] = phone
    session.headers['cat_id'] = cat_id.__str__()
    session.headers['password'] = password
    session.post(server_address)


def add_medication(title: str, description: str, cost: float):
    session.headers['class'] = 'medication'
    session.headers['title'] = encrypted_string(title)
    session.headers['description'] = encrypted_string(description)
    session.headers['cost'] = cost.__str__()
    session.post(server_address)


def add_appointment(time: str, doctor_id: int, cat_id: int, state: str, need_med):
    session.headers['class'] = 'appointment'
    session.headers['time'] = time
    session.headers['doctor_id'] = doctor_id.__str__()
    session.headers['cat_id'] = cat_id.__str__()
    session.headers['state'] = state
    # session.headers['cat_weight'] = cat_weight.__str__()
    session.headers['need_med'] = need_med
    session.post(server_address)


def change_doctor_status(id_doc: int, status: bool):
    session.headers['class'] = 'doctor'
    session.headers['id'] = id_doc.__str__()
    session.headers['status'] = status.__str__()
    session.put(server_address)


def change_medication_cost(id_med: int, cost: float):
    session.headers['class'] = 'medication'
    session.headers['id'] = id_med.__str__()
    session.headers['cost'] = cost.__str__()
    session.put(server_address)


def change_medication(id_med: int, title:str,
                      description: str, cost: float):
    session.headers['class'] = 'change_medication'
    session.headers['id'] = id_med.__str__()
    session.headers['title'] = encrypted_string(title)
    session.headers['description'] = encrypted_string(description)
    session.headers['cost'] = cost.__str__()
    session.put(server_address)


def change_cat(id_cat: int, name: str, age: int, cat_breed: str):
    session.headers['class'] = 'cat'
    session.headers['id'] = id_cat.__str__()
    session.headers['name'] = encrypted_string(name)
    session.headers['age'] = age.__str__()
    session.headers['cat_breed'] = encrypted_string(cat_breed)
    session.put(server_address)

def change_doctor(id_doc: int, fio: str, email: str, phone: str,
                  password: str, work_time, is_chief: bool):
    session.headers['class'] = 'change_doctor'
    session.headers['id'] = id_doc.__str__()
    session.headers['fio'] = encrypted_string(fio)
    session.headers['email'] = encrypted_string(email)
    session.headers['phone'] = phone
    session.headers['password'] = password
    session.headers['work_time'] = work_time
    session.headers['is_chief'] = is_chief.__str__()
    session.put(server_address)

def change_doctor_without_password(id_doc: int, fio: str, email: str, phone: str,
                                   work_time, is_chief: bool):
    session.headers['class'] = 'change_doctor_without_password'
    session.headers['id'] = id_doc.__str__()
    session.headers['fio'] = encrypted_string(fio)
    session.headers['email'] = encrypted_string(email)
    session.headers['phone'] = phone
    session.headers['work_time'] = work_time
    session.headers['is_chief'] = is_chief.__str__()
    session.put(server_address)

def change_client(id_doc: int, fio: str, email: str, phone: str,
                  password: str):
    session.headers['class'] = 'change_client'
    session.headers['id'] = id_doc.__str__()
    session.headers['fio'] = encrypted_string(fio)
    session.headers['email'] = encrypted_string(email)
    session.headers['phone'] = phone
    session.headers['password'] = password
    session.put(server_address)

def delete_doctor(id_doc: int):
    session.headers['class'] = 'doctor'
    session.headers['id'] = id_doc.__str__()
    session.delete(server_address)

def delete_doctor_by_fio(id_doc: int):
    session.headers['class'] = 'doctor_by_fio'
    session.headers['fio'] = id_doc.__str__()
    session.delete(server_address)

def delete_cat(id_cat: int):
    session.headers['class'] = 'cat'
    session.headers['id'] = id_cat.__str__()
    session.delete(server_address)


def delete_client(id_client: int):
    session.headers['class'] = 'client'
    session.headers['id'] = id_client.__str__()
    session.delete(server_address)


def delete_medication(id_medication: int):
    session.headers['class'] = 'medication'
    session.headers['id'] = id_medication.__str__()
    session.delete(server_address)


def delete_appointment(id_app: int):
    session.headers['class'] = 'appointment'
    session.headers['id'] = id_app.__str__()
    session.delete(server_address)


def generate_test_data():
    add_doctor('Bobkov Bob Bobkovich', 'bobemail@test.com', 'bobphone', 'bobpassword', 'bobwork_time', True)
    add_doctor('Natachaovna Natacha Bobkovich', 'natachaemail@test.com', 'natachaphone', 'natachapassword', 'natachawork_time', True)
    add_doctor('Stivov Stiv Stivovich', 'stivemail@test.com', 'stivphone', 'stivpassword', 'stivwork_time', True)
    add_doctor('Tomov Tom Tomovich', 'tomemail@test.com', 'tomphone', 'tompassword', 'tomwork_time', True)

    add_cat('Memesy', 1, 3, 'cat_breed_1')
    add_cat('Tom', 1, 5, 'cat_breed_2')
    add_cat('Masy', 1, 4, 'cat_breed_2')
    add_cat('Mymy', 2, 2, 'cat_breed_3')

    add_medication('med1', 'desription1', 5.5)
    add_medication('med2', 'desription2', 16.3)
    add_medication('med3', 'desription3', 9.4)

    add_client('Bobkov Bob Bobkovich', 'email1@test.com', 'phone1', 1, 'password1')
    add_client('Natachaovna Natacha Bobkovich', 'email2@test.com', 'phone2', 1, 'password2')
    add_client('Tomov Tom Tomovich', 'email3@test.com', 'phone3', 1, 'password3')


def encrypted_string(line: str) -> str:
    line_e = line.encode('utf-8')
    array_bytes = []
    for byte in line_e:
        array_bytes.append(byte)
    result = ""
    for e in array_bytes:
        result += f'*{str(e)}'
    return result[1:]


def decrypt_string(line: str) -> str:
    line_s = line.split('*')
    line_e = []
    for i in range(0, line_s.__len__()):
        line_e.append(int(line_s[i]))
    return bytes(line_e).decode('utf-8')
