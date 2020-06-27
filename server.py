import json
from data_base import Database
from http import server
import hashlib

db = Database()



def start_server():
    Database()
    address_server = ('192.168.1.128', 80)
    httpd = server.HTTPServer(address_server, CustomHandler)
    httpd.serve_forever()


class CustomHandler(server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        if self.headers['class'] == 'doctor':
            self.wfile.write(json.dumps(db.get_all_doctors()).encode("utf-8"))

        elif self.headers['class'] == 'cat':
            self.wfile.write(json.dumps(db.get_all_cats()).encode("utf-8"))

        elif self.headers['class'] == 'client':
            self.wfile.write(json.dumps(db.get_all_clients()).encode("utf-8"))

        elif self.headers['class'] == 'medication':
            self.wfile.write(json.dumps(db.get_all_medications()).encode("utf-8"))

        elif self.headers['class'] == 'my_pets':
            id_client = int(self.headers['id'])
            self.wfile.write(json.dumps(db.get_my_pets(id_client)).encode("utf-8"))
        elif self.headers['class'] == 'my_pet':
            id_client = int(self.headers['id'])
            cat_name = self.decrypt_string(self.headers['cat_name'])
            self.wfile.write(json.dumps(db.get_my_pet(id_client, cat_name)).encode("utf-8"))
        elif self.headers['class'] == 'is_doctor_with_email':
            email = self.decrypt_string(self.headers['email'])
            self.wfile.write(db.is_doctor_with_email(email).__str__().encode("utf-8"))
        elif self.headers['class'] == 'is_client_with_email':
            email = self.decrypt_string(self.headers['email'])
            self.wfile.write(db.is_client_with_email(email).__str__().encode("utf-8"))
        elif self.headers['class'] == 'get_doctor_by_email':
            email = self.decrypt_string(self.headers['email'])
            self.wfile.write(db.get_doctor_by_email(email).__str__().encode("utf-8"))
        elif self.headers['class'] == 'get_client_by_email':
            email = self.decrypt_string(self.headers['email'])
            self.wfile.write(db.get_client_by_email(email).__str__().encode("utf-8"))
        elif self.headers['class'] == 'appointment':
            self.wfile.write(json.dumps(db.get_all_appointments()).encode("utf-8"))
        elif self.headers['class'] == 'get_doctor_by_fio':
            doc_name = self.decrypt_string(self.headers['fio'])
            self.wfile.write(db.get_doctor_by_fio(doc_name).__str__().encode("utf-8"))


    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()

        if self.headers['class'] == 'doctor':
            is_chief = self.headers['is_chief'] == 'True'
            has_password = hashlib.md5(bytes(self.headers['password'], 'utf-8')).hexdigest()
            db.add_doctor(self.decrypt_string(self.headers['fio']), self.decrypt_string(self.headers['email']),
                          self.headers['phone'], has_password, self.headers['work_time'], is_chief)

        elif self.headers['class'] == 'cat':
            db.add_cat(self.decrypt_string(self.headers['name']), int(self.headers['owner_id']),
                       int(self.headers['age']), self.decrypt_string(self.headers['cat_breed']))

        elif self.headers['class'] == 'client':
            has_password = hashlib.md5(bytes(self.headers['password'], 'utf-8')).hexdigest()
            db.add_client(self.decrypt_string(self.headers['fio']), self.decrypt_string(self.headers['email']),
                          self.headers['phone'], int(self.headers['cat_id']),
                          has_password)

        elif self.headers['class'] == 'medication':
            db.add_medication(self.decrypt_string(self.headers['title']), self.decrypt_string(self.headers['description']),
                              self.headers['cost'])

        elif self.headers['class'] == 'appointment':
            db.add_appointment(self.headers['time'], int(self.headers['doctor_id']), int(self.headers['cat_id']),
                               self.headers['state'], self.headers['need_med'])

        self.wfile.write(json.dumps({'result': True}).encode())

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()

        if self.headers['class'] == 'doctor':
            db.delete_doctor(int(self.headers['id']))

        elif self.headers['class'] == 'cat':
            db.delete_cat(int(self.headers['id']))

        elif self.headers['class'] == 'client':
            db.delete_client(int(self.headers['id']))

        elif self.headers['class'] == 'medication':
            db.delete_medication(int(self.headers['id']))

        elif self.headers['class'] == 'appointment':
            db.delete_appointment(int(self.headers['id']))

        elif self.headers['class'] == 'doctor_by_fio':
            db.doctor_by_fio(self.headers['fio'])

        self.wfile.write(b'DELETE request\n')

    def do_PUT(self):
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()

        if self.headers['class'] == 'doctor':
            status = self.headers['status'] == 'True'
            db.change_doctor_status(self.headers['id'], status)

        elif self.headers['class'] == 'medication':
            db.change_medication_cost(int(self.headers['id']), float(self.headers['cost']))

        elif self.headers['class'] == 'cat':
            db.change_cat(int(self.headers['id']), self.decrypt_string(self.headers['name']),
                          self.headers['age'], self.decrypt_string(self.headers['cat_breed']))

        elif self.headers['class'] == 'change_doctor':
            is_chief = self.headers['is_chief'] == 'True'
            has_password = hashlib.md5(bytes(self.headers['password'], 'utf-8')).hexdigest()
            db.change_doctor(int(self.headers['id']), self.decrypt_string(self.headers['fio']),
                          self.decrypt_string(self.headers['email']), self.headers['phone'],
                             has_password, self.headers['work_time'], is_chief)

        elif self.headers['class'] == 'change_doctor_without_password':
            is_chief = self.headers['is_chief'] == 'True'
            db.change_doctor_without_password(int(self.headers['id']), self.decrypt_string(self.headers['fio']),
                          self.decrypt_string(self.headers['email']), self.headers['phone'],
                             self.headers['work_time'], is_chief)

        elif self.headers['class'] == 'change_medication':
            db.change_medication(int(self.headers['id']), self.decrypt_string(self.headers['title']),
                          self.decrypt_string(self.headers['description']), self.headers['cost'])

        elif self.headers['class'] == 'change_client':
            has_password = hashlib.md5(bytes(self.headers['password'], 'utf-8')).hexdigest()
            db.change_client(int(self.headers['id']), self.decrypt_string(self.headers['fio']),
                             self.decrypt_string(self.headers['email']), self.headers['phone'],
                             has_password)

        self.wfile.write(b'PUT request\n')

    def decrypt_string(self, line: str) -> str:
        line_s = line.split('*')
        line_e = []
        for i in range(0, line_s.__len__()):
            line_e.append(int(line_s[i]))
        return bytes(line_e).decode('utf-8')


server_address = ('192.168.1.128', 80)
httpd = server.HTTPServer(server_address, CustomHandler)
print('Start server')
httpd.serve_forever()
