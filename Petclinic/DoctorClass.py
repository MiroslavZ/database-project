from Petclinic.PetclinicExeptions import *


class DoctorClass:
    id = 0
    fio = ""
    email = ""
    phone = ""
    password = ""
    work_time = None
    is_chief = False

    def __init__(self, id: int, fio: str, email: str, phone: str, password: str, work_time, is_chief: bool):
        self.id = id
        self.fio = fio
        self.email = email
        self.phone = phone
        self.password = password
        self.work_time = work_time
        self.is_chief = is_chief

    @staticmethod
    def decrypt(data: str):
        data_s = data.split('**')
        is_chief = data_s[6] == "True"
        doc = DoctorClass(int(data_s[0]), data_s[1], data_s[2], data_s[3],
                          data_s[4], data_s[5].__str__(), is_chief)
        return doc

    def getId(self):
        return self.id

    def setFio(self, fio: str):
        if fio.__eq__("") or fio is None:
            raise ChangeAtributeException
        self.fio = fio

    def getFio(self):
        return self.fio

    def setEmail(self, email: str):
        if email.__eq__("") or email is None:
            raise ChangeAtributeException
        self.email = email

    def getEmail(self):
        return self.email

    def setPhone(self, phone: str):
        if phone.__eq__("") or phone is None:
            raise ChangeAtributeException
        self.phone = phone

    def getPhone(self):
        return self.phone

    def setPassword(self, password: str):
        if password is None:
            raise ChangeAtributeException
        self.password = password

    def getPassword(self):
        return self.password

    def setWorkTime(self,work_time):
        self.work_time=work_time

    def getWorkTime(self):
        return self.work_time

    def setIsChief(self, is_chief:bool):
        self.is_chief = is_chief

    def getIsChief(self):
        return self.is_chief

    def __eq__(self, other):
        if type(other) != DoctorClass:
            return False
        return self.fio == other.fio and \
               self.email == other.email and \
               self.phone == other.phone and \
               self.password == other.password and \
               self.work_time == other.work_time and \
               self.is_chief == other.is_chief

    def __str__(self):
        return self.id.__str__() + '**' + self.fio + '**' + self.email \
               + '**' + self.phone + '**' + self.password + '**' \
               + self.work_time.__str__() + '**' + self.is_chief.__str__()
