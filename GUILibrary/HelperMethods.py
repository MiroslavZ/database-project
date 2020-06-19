import re
import datetime


#различные вспомогательные методы и проверки
def check_correct_email(text:str)->bool:
    pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
    is_valid = pattern.match(text)
    return is_valid


def check_correct_name(text:str)->bool:
    if len(text) > 1:
        match1 = re.match("^[АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]*$", text[0])
        match2 = re.match("^[абвгдеёжзиклмнопрстуфхцчшщъыьэюя]*$", text[1:])
        return match1 is not None and match2 is not None


def check_correct_phone(text:str)->bool:
    match = re.match("^[0123456789]*$", text)
    return match is not None and len(text) == 11


def check_correct_password(text:str)->bool:
    return len(text) > 0


def check_correct_worktime(text:str)->bool:
    # будь прокляты регулярные выражения!
    if len(text)>2 and len(text)<6:
        temp=text.split(":")
        if len(temp)==2:
            if temp[0].isdigit() and temp[1].isdigit():
                hour = int(temp[0])
                print("hour is "+str(hour))
                minute = int(temp[1])
                print("minute is "+str(minute))
                return hour >= 0 and hour < 24 and minute >= 0 and minute < 60
    return False


def parse_work_time(text:str):
    if check_correct_worktime(text):
        print("split...")
        result=text.split(":")
        print("result:")
        print(result)
        return result
    return None


def deparse_work_time(time:datetime.time)->str:
    return str(time.hour)+":"+str(time.minute)