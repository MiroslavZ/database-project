import requests
import json

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


def get_my_pets(id_client: int):
    session.headers['class'] = 'my_pets'
    session.headers['id'] = id_client.__str__()
    cats_encrypted = json.loads(session.get(server_address).text)
    cats_decrypted = {}
    for key in cats_encrypted:
        cat = CatClass.decrypt(cats_encrypted[key])
        cats_decrypted[cat.id] = cat
    return cats_decrypted


def add_doctor(fio: str, email: str, phone: str,
               password: str, work_time, is_chief: bool):
    session.headers['class'] = 'doctor'
    session.headers['fio'] = fio
    session.headers['email'] = email
    session.headers['phone'] = phone
    session.headers['password'] = password
    session.headers['work_time'] = work_time
    session.headers['is_chief'] = is_chief.__str__()
    session.post(server_address)


def add_cat(name: str, owner_id: int, age: int, cat_breed: str):
    session.headers['class'] = 'cat'
    session.headers['name'] = name
    session.headers['owner_id'] = owner_id.__str__()
    session.headers['age'] = age.__str__()
    session.headers['cat_breed'] = cat_breed
    session.post(server_address)


def add_client(fio: str, email: str, phone: str, cat_id: int, password: str):
    session.headers['class'] = 'client'
    session.headers['fio'] = fio
    session.headers['email'] = email
    session.headers['phone'] = phone
    session.headers['cat_id'] = cat_id.__str__()
    session.headers['password'] = password
    session.post(server_address)


def add_medication(title: str, description: str, cost: float):
    session.headers['class'] = 'medication'
    session.headers['title'] = title
    session.headers['description'] = description
    session.headers['cost'] = cost.__str__()
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


def delete_doctor(id_doc: int):
    session.headers['class'] = 'doctor'
    session.headers['id'] = id_doc.__str__()
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
