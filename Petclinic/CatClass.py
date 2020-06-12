import json

from Petclinic.PetclinicExeptions import *


class CatClass:
    id = 0
    name = ""
    owner_id = 0
    age = 0
    cat_breed = ""

    def __init__(self, id: int, name: str, owner_id: int, age: int, cat_breed: str):
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.age = age
        self.cat_breed = cat_breed

    @staticmethod
    def decrypt(data: str):
        data_s = data.split('**')
        cat = CatClass(int(data_s[0]), data_s[1], int(data_s[2]), int(data_s[3]), data_s[4])
        return cat

    def getId(self):
        return self.id

    def setName(self, name: str):
        if name.__eq__(""):
            raise ChangeAtributeException
        self.name = name

    def getName(self):
        return self.name

    def setOwner(self, owner_id: int):
        self.owner_id = owner_id

    def getOwner(self):
        return self.owner_id

    def setAge(self, age: int):
        if age < 0:
            raise ChangeAtributeException
        self.age = age

    def getAge(self):
        return self.age

    def setCatBreed(self, cat_breed: str):
        self.cat_breed = cat_breed

    def getCatBreed(self):
        return self.cat_breed

    def __eq__(self, other):
        if type(other) != CatClass:
            return False
        return self.name == other.name and self.owner_id == other.owner_id and \
               self.age == other.age and self.cat_breed == other.cat_breed

    def __str__(self):
        return self.id.__str__() + '**' + self.name + '**' + self.owner_id.__str__() \
               + '**' + self.age.__str__() + '**' + self.cat_breed

# class CatClassEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, CatClass):
#             return obj.__dict__
#         return json.JSONEncoder.default(self, obj)
