import unittest
import main
import client
from Petclinic.CatClass import CatClass
from Petclinic.ClientClass import ClientClass
from Petclinic.DoctorClass import DoctorClass
from Petclinic.MedicationClass import MedicationClass


class TestServerClient(unittest.TestCase):

    def setUp(self) -> None:
        main.Database.recreate_tables()

    def test_AddOneDoctor(self):
        client.add_doctor('fio', 'email', 'phone', 'password', 'work_time', False)
        dict_doctors = client.get_all_doctors()
        self.assertEqual(1, dict_doctors.__len__())
        expect = DoctorClass(1, 'fio', 'email', 'phone', 'password', 'work_time', False)
        self.assertEqual(expect, dict_doctors[1])

    def test_AddTwoDoctor(self):
        client.add_doctor('fio', 'email', 'phone', 'password', 'work_time', False)
        client.add_doctor('fio2', 'email2', 'phone2', 'password2', 'work_time2', True)
        dict_doctors = client.get_all_doctors()

        self.assertEqual(2, dict_doctors.__len__())

        expect = DoctorClass(1, 'fio', 'email', 'phone', 'password', 'work_time', False)
        self.assertEqual(expect, dict_doctors[1])
        expect = DoctorClass(1, 'fio2', 'email2', 'phone2', 'password2', 'work_time2', True)
        self.assertEqual(expect, dict_doctors[2])

    def test_AddOneCat(self):
        client.add_cat('fio', 2, 3, 'cat_breed')
        dict_cats = client.get_all_cats()
        self.assertEqual(1, dict_cats.__len__())
        expect = CatClass(1, 'fio', 2, 3, 'cat_breed')
        self.assertEqual(expect, dict_cats[1])

    def test_AddTwoCat(self):
        client.add_cat('fio', 2, 3, 'cat_breed')
        client.add_cat('fio2', 5, 4, 'cat_breed2')
        dict_cats = client.get_all_cats()

        self.assertEqual(2, dict_cats.__len__())

        expect = CatClass(0, 'fio', 2, 3, 'cat_breed')
        self.assertEqual(expect, dict_cats[1])
        expect = CatClass(0, 'fio2', 5, 4, 'cat_breed2')
        self.assertEqual(expect, dict_cats[2])

    def test_AddOneMedication(self):
        client.add_medication('title', 'description', 1.5)
        dict_medications = client.get_all_medications()

        self.assertEqual(1, dict_medications.__len__())

        expect = MedicationClass(0, 'title', 'description', 1.5)
        self.assertEqual(expect, dict_medications[1])

    def test_AddTwoMedication(self):
        client.add_medication('title', 'description', 1.5)
        client.add_medication('title2', 'description2', 2.5)
        dict_medications = client.get_all_medications()

        self.assertEqual(2, dict_medications.__len__())

        expect = MedicationClass(0, 'title', 'description', 1.5)
        self.assertEqual(expect, dict_medications[1])
        expect = MedicationClass(0, 'title2', 'description2', 2.5)
        self.assertEqual(expect, dict_medications[2])

    def test_AddOneClient(self):
        client.add_client('fio', 'email', 'phone', 1, 'password')
        dict_clients = client.get_all_clients()

        self.assertEqual(1, dict_clients.__len__())

        expect = ClientClass(1, 'fio', 'email', 'phone', 1, 'password')
        self.assertEqual(expect, dict_clients[1])

    def test_AddTwoClient(self):
        client.add_client('fio', 'email', 'phone', 1, 'password')
        client.add_client('fio2', 'email2', 'phone2', 2, 'password2')
        dict_clients = client.get_all_clients()

        self.assertEqual(2, dict_clients.__len__())

        expect = ClientClass(0, 'fio', 'email', 'phone', 1, 'password')
        self.assertEqual(expect, dict_clients[1])
        expect = ClientClass(0, 'fio2', 'email2', 'phone2', 2, 'password2')
        self.assertEqual(expect, dict_clients[2])

    def test_DeleteOneDoctor(self):
        client.add_doctor('fio', 'email', 'phone', 'password', 'work_time', True)
        id_doctor = 1
        client.delete_doctor(id_doctor)
        dict_doctors = client.get_all_doctors()
        self.assertEqual(0, dict_doctors.__len__())

    def test_DeleteTwoDoctor(self):
        client.add_doctor('fio', 'email', 'phone', 'password', 'work_time', True)
        client.add_doctor('fio2', 'email2', 'phone2', 'password2', 'work_time2', False)
        id_doctor = 1
        client.delete_doctor(id_doctor)
        id_doctor = 2
        client.delete_doctor(id_doctor)
        list_doctors = client.get_all_doctors()
        self.assertEqual(0, list_doctors.__len__())

    def test_DeleteOneCat(self):
        client.add_cat('fio', 2, 3, 'cat_breed')
        client.delete_cat(1)
        dict_cats = client.get_all_cats()
        self.assertEqual(0, dict_cats.__len__())

    def test_DeleteTwoCat(self):
        client.add_cat('fio', 2, 3, 'cat_breed')
        client.add_cat('fio2', 5, 4, 'cat_breed2')
        client.delete_cat(1)
        client.delete_cat(2)
        list_cats = client.get_all_cats()
        self.assertEqual(0, list_cats.__len__())

    def test_DeleteOneMedication(self):
        client.add_medication('title', 'description', 1.5)
        client.delete_medication(1)
        list_med = client.get_all_medications()
        self.assertEqual(0, list_med.__len__())

    def test_DeleteTwoMedication(self):
        client.add_medication('title', 'description', 1.5)
        client.add_medication('title2', 'description2', 1.5)
        client.delete_medication(1)
        client.delete_medication(2)
        list_med = client.get_all_medications()
        self.assertEqual(0, list_med.__len__())

    def test_DeleteOneClient(self):
        client.add_client('fio', 'email', 'phone', 1, 'password')
        client.delete_client(1)
        list_clients = client.get_all_clients()
        self.assertEqual(0, list_clients.__len__())

    def test_DeleteTwoClient(self):
        client.add_client('fio', 'email', 'phone', 1, 'password')
        client.add_client('fio2', 'email2', 'phone2', 2, 'password2')
        client.delete_client(1)
        client.delete_client(2)
        list_clients = client.get_all_clients()
        self.assertEqual(0, list_clients.__len__())

    def test_ChangeMedicationCost(self):
        client.add_medication('title', 'description', 1.5)
        id_med = 1
        client.change_medication_cost(id_med, 333.33)

        dict_medications = client.get_all_medications()

        expect = MedicationClass(0, 'title', 'description', 333.33)
        self.assertEqual(expect, dict_medications[1])

    def test_ChangeDoctorStatus(self):
        client.add_doctor('fio', 'email', 'phone', 'password', 'work_time', False)
        id_doctor = 1
        client.change_doctor_status(id_doctor, True)
        dict_doctors = client.get_all_doctors()
        expect = DoctorClass(0, 'fio', 'email', 'phone', 'password', 'work_time', True)
        self.assertEqual(expect, dict_doctors[1])

    def test_GetMyPetsOnOnePet(self):
        client.add_client('fio', 'email', 'phone', 1, 'password')
        client.add_cat('fio', 1, 3, 'cat_breed')
        dict_cats = client.get_my_pets(1)

        self.assertEqual(1, dict_cats.__len__())

        expect = CatClass(0, 'fio', 1, 3, 'cat_breed')
        self.assertEqual(expect, dict_cats[1])

    def test_GetMyPetsOnTwoPets(self):
        client.add_client('fio', 'email', 'phone', 1, 'password')
        client.add_cat('fio', 1, 3, 'cat_breed')
        client.add_cat('fio2', 1, 4, 'cat_breed2')
        dict_cats = client.get_my_pets(1)

        self.assertEqual(2, dict_cats.__len__())

        expect = CatClass(0, 'fio', 1, 3, 'cat_breed')
        self.assertEqual(expect, dict_cats[1])
        expect = CatClass(0, 'fio2', 1, 4, 'cat_breed2')
        self.assertEqual(expect, dict_cats[2])


if __name__ == '__main__':
    unittest.main()
