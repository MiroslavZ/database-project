import json
import main
from http import server

db = main.Database()


def start_server():
    main.Database()
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

    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()

        if self.headers['class'] == 'doctor':
            is_chief = self.headers['is_chief'] == 'True'
            db.add_doctor(self.headers['fio'], self.headers['email'],
                          self.headers['phone'], self.headers['password'],
                          self.headers['work_time'], is_chief)

        elif self.headers['class'] == 'cat':
            db.add_cat(self.headers['name'], self.headers['owner_id'],
                       self.headers['age'], self.headers['cat_breed'])

        elif self.headers['class'] == 'client':
            db.add_client(self.headers['fio'], self.headers['email'],
                          self.headers['phone'], self.headers['cat_id'],
                          self.headers['password'])

        elif self.headers['class'] == 'medication':
            db.add_medication(self.headers['title'], self.headers['description'],
                              self.headers['cost'])

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

        self.wfile.write(b'PUT request\n')


# В ковычках пишешь свой ip
server_address = ('192.168.1.128', 80)
httpd = server.HTTPServer(server_address, CustomHandler)
print('Start server')
httpd.serve_forever()
