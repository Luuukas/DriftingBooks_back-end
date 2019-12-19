from datetime import datetime
from UserModel.models import User
import ust_handler

def add_user(username, password, phonenumber):
    try:
        user = User(username=username, password=password, phonenumber=phonenumber, enrolldatetime=datetime.now())
        user.save()
    except BaseException:
        return {"state":1}
    else:
        ust_handler.create_stars_table(user.uid)
        return {"state":0}

def del_user(uid):
    try:
        user = User.objects.get(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        user.delete()
        ust_handler.delete_stars_table(uid)
        return {"state":0}

def check_user_with_username(username, password):
    try:
        user = User.objects.get(username=username)
    except BaseException:
        return {"state":1}
    else:
        if user.password==password:
            return {
                "state" : 0,
                "uid" : user.uid
            }
        else:
            return {"state":2}

def check_user_with_phonenumber(phonenumber, password):
    try:
        user = User.objects.get(phonenumber=phonenumber)
    except BaseException:
        return {"state":1}
    else:
        if user.password==password:
            return {
                "state" : 0 ,
                "uid" : user.uid
            }
        else:
            return {"state":2}

def update_password(uid, new_password):
    try:
        user = User.objects.get(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        user.password = new_password
        user.save()
        return {"state":0}

def update_phonenumber(uid, new_phonenumber):
    try:
        user = User.objects.get(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        user.phonenumber = new_phonenumber
        user.save()
        return {"state":0}

def update_address(uid, new_address):
    try:
        user = User.objects.get(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        user.address = new_address
        user.save()
        return {"state":0}

def increase_credit(uid, delta):
    try:
        user = User.objects.get(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        if user.address == "":
            return {"state":3}
        if user.credit+delta < 0:
            return {"state":2}
        user.credit += delta
        user.save()
        return {"state":0, "infos":[user.username, user.phonenumber, user.address]}

def get_user_infos(uid):
    try:
        user = User.objects.get(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        return {
            "state":0,
            "infos":[user.username, user.phonenumber, user.address, user.credit, user.enrolldatetime]
            }

def get_phonenumber(uid):
    try:
        user = User.objects.get(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        return {
            "state":0,
            "phonenumber":user.phonenumber
        }