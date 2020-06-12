from Petclinic.PetclinicExeptions import *


class MedicationClass:
    id = 0
    title = ""
    description = ""
    cost = 0.0

    def __init__(self, id_med: int, title: str, description: str, cost: float):
        self.id = id_med
        self.title = title
        self.description = description
        self.cost = cost

    @staticmethod
    def decrypt(data: str):
        data_s = data.split('**')
        medication = MedicationClass(int(data_s[0]), data_s[1], data_s[2], float(data_s[3]))
        return medication

    def getId(self):
        return self.id

    def getTitle(self):
        return self.title

    def setTitle(self, title: str):
        if title.__eq__(""):
            raise ChangeAtributeException
        self.title = title

    def getDescription(self):
        return self.description

    def setDescription(self, description: str):
        if description.__eq__(""):
            raise ChangeAtributeException
        self.description = description

    def getCost(self):
        return self.title

    def setCost(self, cost):
        if cost == 0:
            raise ChangeAtributeException
        self.cost = cost

    def __eq__(self, other):
        if type(other) != MedicationClass:
            return False
        return self.title == other.title and \
               self.description == other.description and \
               self.cost == other.cost

    def __str__(self):
        return self.id.__str__() + '**' + self.title + '**' + self.description \
               + '**' + self.cost.__str__()
