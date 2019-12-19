from BottleModel.models import Bottle
from datetime import datetime
import ust_handler
import os
from django.conf import settings

def bottle_cnt():
    return Bottle.objects.all().count()

def add_bottle(uid, bookname, writer, press, description_url, photos_urls_str, timeouthandle, sendto):
    bottle = Bottle(uid=uid, bookname=bookname, writer=writer, press=press, description=description_url, photos=photos_urls_str, timeouthandle=timeouthandle, sendto=sendto, uploaddatetime=datetime.now())
    bottle.save()
    return {"state":0, "botid":bottle.botid}

def del_bottle(botid):
    try:
        bottle = Bottle.objects.get(botid=botid);
    except BaseException:
        return {"state":1}
    else:
        bottle.delete()
        return {"state":0}

def vis_bottle(idx):
    try:
        bottle = Bottle.objects.all()[idx-1];
    except BaseException:
        return {"state":1}
    else:
        return {"state":0, "infos":[bottle.botid, bottle.bookname, bottle.writer, bottle.press, bottle.description, bottle.photos, bottle.timeouthandle, bottle.sendto, bottle.uploaddatetime, bottle.state]}


def get_bottle(botid):
    try:
        bottle = Bottle.objects.get(botid=botid);
    except BaseException:
        return {"state":1}
    else:
        return {"state":0, "infos":[bottle.botid, bottle.bookname, bottle.writer, bottle.press, bottle.description, bottle.photos, bottle.timeouthandle, bottle.sendto, bottle.uploaddatetime, bottle.state]}

def update_description(botid, new_description_url):
    try:
        bottle = Bottle.objects.get(botid=botid)
    except BaseException:
        return {"state":1}
    else:
        file_path = os.path.join(settings.BASE_DIR, 'statics', 'descriptions', bottle.description)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            return {"state":2}
        bottle.description = new_description_url
        bottle.save()
        return {"state":0}

def before_update_sendto(botid, code):
    try:
        bottle = Bottle.objects.get(botid=botid)
    except BaseException:
        return {"state":1}
    else:
        if bottle.state!=2:
            return {"state":2}
        return {"state":0}

def update_sendto(botid, code):
    bottle = Bottle.objects.get(botid=botid)
    bottle.sendto = code
    bottle.save()
    update_state(botid, 4)
    return {"state":0}
        

def update_timeouthandle(botid, new_choice):
    try:
        bottle = Bottle.objects.get(botid=botid)
    except BaseException:
        return {"state":1}
    else:
        if bottle.sendto!=0:
            return {"state":2}
        bottle.timeouthandle = new_choice
        bottle.save()
        return {"state":0}

def update_state(botid, new_state):
    try:
        bottle = Bottle.objects.get(botid=botid)
    except BaseException:
        return {"state":1}
    else:
        bottle.state = new_state
        bottle.save()
        return {"state":0}

def get_can_donate_books():
    pass