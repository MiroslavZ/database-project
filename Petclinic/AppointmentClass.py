class AppointmentClass:
    id = 0
    time = None
    doctor = None
    cat = None
    state = ""
    cat_weight = 0.0
    need_med = None

    def __init__(self, id: int, time, doctor, cat, state, cat_weight, need_med):
        self.id = id
        self.time = time
        self.doctor = doctor
        self.cat = cat
        self.state = state
        self.cat_weight = cat_weight
        self.need_med = need_med

    def getId(self):
        return self.id

    def getTime(self):
        return self.time

    def setTime(self, time):
        self.time = time

    def getDoctor(self):
        return self.doctor

    def setDoctor(self, doctor):
        self.doctor = doctor

    def getCat(self):
        return self.cat

    def setCat(self, cat):
        self.cat = cat

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
        return self.time == other.time and\
               self.doctor == other.doctor and\
               self.cat == other.cat and\
               self.state == other.state and\
               self.cat_weight == other.cat_weight and\
               self.need_med == other.need_med
