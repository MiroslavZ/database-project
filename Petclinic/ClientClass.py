from Petclinic.PetclinicExeptions import *


class ClientClass:
    id = 0
    fio = ""
    email = ""
    phone = ""
    cat_id = ""
    password = ""

    def __init__(self, id: int, fio: str, email: str, phone: str, cat_id: int, password: str):
        self.id = id
        self.fio = fio
        self.email = email
        self.phone = phone
        self.cat_id = cat_id
        self.password = password

    @staticmethod
    def decrypt(data: str):
        data_s = data.split('**')
        client = ClientClass(int(data_s[0]), data_s[1], data_s[2], data_s[3], int(data_s[4]), data_s[5])
        return client

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

    def setPnone(self, phone: str):
        if phone.__eq__("") or phone is None:
            raise ChangeAtributeException
        self.phone = phone

    def getPhone(self):
        return self.phone

    def setCat(self, cat):
        if cat is None:
            raise ChangeAtributeException
        self.cat_id = cat

    def getCat(self):
        return self.cat_id

    def setPassword(self, password: str):
        if password is None:
            raise ChangeAtributeException
        self.password = password

    def getPassword(self):
        return self.password

    def __eq__(self, other):
        if type(other) != ClientClass:
            return False
        return self.fio == other.fio and \
               self.email == other.email and \
               self.phone == other.phone and \
               self.cat_id == other.cat_id

    def __str__(self):
        return self.id.__str__() + '**' + self.fio + '**' + self.email \
               + '**' + self.phone + '**' + self.cat_id.__str__() + '**' + self.password
