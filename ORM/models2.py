import sqlite3

conn = sqlite3.connect("petclinic.db")
cursor = conn.cursor()

def CreateTableClients():
    cursor.execute("""CREATE TABLE clients
                           (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                           fio text, email text, phone text, cat text, password text)
                       """)


def CreateTableCats():
    cursor.execute("""CREATE TABLE cats
                           (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                           name text, owner_id INT, age INT, cat_breed text,
                           FOREIGN KEY (owner_id) REFERENCES clients(id))
                       """)


def CreateTableDoctors():
    cursor.execute("""CREATE TABLE doctors
                           (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                           fio text, email text, phone text, password text, work_time BLOB, is_chief BOOLEAN)
                       """)


def CreateTableMedications():
    cursor.execute("""CREATE TABLE medications
                           (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                           title text, description text, cost INT)
                       """)


def CreateTableAppointments():
    cursor.execute("""CREATE TABLE appointments
                           (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                           time text, doctor_id INT, cat_id INT, state text, need_med INT,
                           FOREIGN KEY (doctor_id) REFERENCES doctor(id),
                           FOREIGN KEY (cat_id) REFERENCES cat(id),
                           FOREIGN KEY (need_med) REFERENCES Medication(id))
                       """)

def create_tables():
    CreateTableClients()
    CreateTableCats()
    CreateTableDoctors()
    CreateTableMedications()
    CreateTableAppointments()

def drop_all_tables():
    cursor.execute("DROP TABLE clients")
    cursor.execute("DROP TABLE cats")
    cursor.execute("DROP TABLE doctors")
    cursor.execute("DROP TABLE medications")
    cursor.execute("DROP TABLE appointments")

