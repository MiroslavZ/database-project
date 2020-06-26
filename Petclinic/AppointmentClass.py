class AppointmentClass:
    id = 0
    time = None
    doctor_id = 0
    cat_id = 0
    state = ""
    cat_weight = 0.0
    need_med = None

    def __init__(self, app_id: int, time: str, doctor_id: int, cat_id: int, state: str, need_med):
        self.id = app_id
        self.time = time
        self.doctor_id = doctor_id
        self.cat_id = cat_id
        self.state = state
        # self.cat_weight = cat_weight
        self.need_med = need_med

    @staticmethod
    def decrypt(data: str):
        data_s = data.split('**')
        appointment = AppointmentClass(int(data_s[0]), data_s[1], int(data_s[2]), int(data_s[3]),
                                       data_s[4], data_s[5])
        return appointment

    def getId(self):
        return self.id

    def getTime(self):
        return self.time

    def setTime(self, time):
        self.time = time

    def getDoctorId(self):
        return self.doctor_id

    def setDoctorId(self, doctor_id: int):
        self.doctor_id = doctor_id

    def getCatId(self):
        return self.cat_id

    def setCatId(self, cat_id):
        self.cat_id = cat_id

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getCatWeight(self):
        return self.cat_weight

    def setCatWeight(self, cat_weight):
        self.cat_weight = cat_weight

    def getNeedMed(self):
        return self.need_med

    def setNeedMed(self, need_med):
        self.need_med = need_med

    def __eq__(self, other):
        if type(other) != AppointmentClass:
            return False
        return self.time == other.time and \
               self.doctor_id == other.doctor and \
               self.cat_id == other.cat and \
               self.state == other.state and \
               self.need_med == other.need_med
        # self.cat_weight == other.cat_weight and \

    def __str__(self):
        return self.id.__str__() + '**' + self.time + '**' + self.doctor_id.__str__() \
               + '**' + self.cat_id.__str__() + '**' + self.state + '**' + self.need_med
