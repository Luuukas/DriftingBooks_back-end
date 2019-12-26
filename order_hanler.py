from OrderModel.models import Order
from datetime import datetime
import time
def get_order_code():
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
    return order_no

def append_receive_order(uid, expresscompany, trackingnumber, botid, address, name, phonenumber):
    try:
        order = Order(oid="A"+get_order_code(), uid=uid, otype=0, expresscompany=expresscompany, trackingnumber=trackingnumber, botid=botid, address=address, name=name, phonenumber=phonenumber, state=0, submittime=datetime.now())
        order.save();
    except BaseException:
        return {"state":1}
    else:
        return {
            "state":0,
            "oid":order.oid
            }

def append_sent_order(otype, uid, botid, address, name, phonenumber):
    try:
        order = Order(oid=("B" if(otype==1) else "C")+get_order_code(), uid=uid, otype=otype, botid=botid, address=address, phonenumber=phonenumber, name=name, state=0, submittime=datetime.now())
        order.save();
    except BaseException:
        return {"state":1}
    else:
        return {
            "state":0,
            "oid":order.oid
            }

def fill_sent_order(oid, expresscompany, trackingnumber):
    try:
        order = Order.objects.get(oid=oid)
    except BaseException:
        return {"state":1}
    else:
        if not order.state==0: return {"state":2}
        order.expresscompany = expresscompany
        order.trackingnumber = trackingnumber
        order.completetime = datetime.now()
        order.state = 1
        order.save()
        return {"state":0}

def update_state(oid):
    try:
        order = Order.objects.get(oid=oid)
    except BaseException:
        return {"state":1}
    else:
        order.state = 1
        order.completetime = datetime.now()
        order.save()
        return {"state":0}

def get_all_order():
    try:
        orders = Order.objects.all()
    except BaseException:
        return {"state":1}
    else:
        allorder = []
        for order in orders:
            allorder.append({
                "oid" : order.oid,
                "otype" : order.otype,
                "state" : order.state,
                "expresscompany" : order.expresscompany,
                "trackingnumber" : order.trackingnumber,
                "address" : order.address,
                "name" : order.name,
                "phonenumber" : order.phonenumber,
                "submittime" : str(order.submittime),
                "completetime" : str(order.completetime)
            })
        return {"state":0, "orders":allorder}

def get_order_with_oid(oid):
    try:
        order = Order.objects.get(oid=oid)
    except BaseException:
        return {"state":1}
    else:
        return {
            "state" : 0,
            "infos" : {
                "oid" : order.oid,
                "otype" : order.otype,
                "state" : order.state,
                "expresscompany" : order.expresscompany,
                "trackingnumber" : order.trackingnumber,
                "address" : order.address,
                "name" : order.name,
                "phonenumber" : order.phonenumber,
                "submittime" : str(order.submittime),
                "completetime" : str(order.completetime)
            }
            }
import book_handler
import bottle_handler
def get_order_with_uid(uid):
    try:
        orders = Order.objects.filter(uid=uid)
    except BaseException:
        return {"state":1}
    else:
        allorder = []
        for order in orders:
            botid = order.botid
            bottle = bottle_handler.get_bottle(botid)
            book = book_handler.get_book(bottle["infos"][1],bottle["infos"][2],bottle["infos"][3])
            allorder.append({
                "oid" : order.oid,
                "otype" : order.otype,
                "state" : order.state,
                "expresscompany" : order.expresscompany,
                "trackingnumber" : order.trackingnumber,
                "address" : order.address,
                "name" : order.name,
                "phonenumber" : order.phonenumber,
                "submittime" : str(order.submittime),
                "completetime" : str(order.completetime),
                "bookinfos" : {
                    'bookname': book["infos"][1],
                    'writer': book["infos"][2],
                    'press': book["infos"][3],
                    'neededcredit': book["infos"][4],
                    'coverurl': book["infos"][5],
                    'description': book["infos"][6]
                    }
            })
        return {"state":0, "orders":allorder}