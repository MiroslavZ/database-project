import main

db = main.Database('mydatbase.db')
db.add_doctor('fio', 'email', 'phone', 'password', 'work_time', True)
l = db.get_all_doctors()
print(l[0].fio)
print(l[0].email)
print(l[0].phone)
print(l[0].password)
print(l[0].work_time)
print(l[0].is_chief)
print(l)
