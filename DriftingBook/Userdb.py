from django.http import HttpResponse
from django.http import JsonResponse

from UserModel.models import User

import json

import user_handler
import book_handler
import bottle_handler
import ust_handler

import os

from django.conf import settings

import time

from django.core.cache import cache
from django.views.decorators.cache import cache_page

import order_hanler

def addBook(request):
    if(request.method == 'POST'):
        postBody = request.body
        json_result = json.loads(postBody)
        book_handler.add_book(json_result["bookname"], json_result["writer"], json_result["press"], json_result["neededcredit"])
        return HttpResponse(json.dumps({ "msg" : "success" }), content_type="application/json")

def upload(request):
    if request.method == 'POST':
        file_txt = request.POST.get('file_txt')
        print(file_txt)
        file_obj = request.FILES.get('file_obj')
        # 这里的file_obj拿到了文件的对象，这个对象包含了文件的名字，二进制内容
        # print(file_obj, type(file_obj))
        file_name = file_obj.name
        import os
        file_path = os.path.join(settings.BASE_DIR, 'static', 'img', file_obj.name)
        # 这里file_path是存储文件的路径
        # print(settings.BASE_DIR)
 
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse('ok')

def addBottle(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        bookname = request.POST.get('bookname')
        writer = request.POST.get('writer')
        press = request.POST.get('press')
        timeouthandle = (request.POST.get('timeouthandle')=='true')
        sendto =  request.POST.get('sendto')
        sendto = -int(sendto);
        # 把文本写入txt存起来
        description = request.POST.get('description')
        des_name = "des_"+str(time.time())+".txt"
        des_path = os.path.join(settings.BASE_DIR, 'static', 'des', des_name)
        with open(des_path, 'w') as f:
            f.write(description)
        
        # 获取图片
        try:
            img_obj = request.FILES.get('img_obj')
            # 这里的file_obj拿到了文件的对象，这个对象包含了文件的名字，二进制内容
            # 获取文件后缀名
            postfix = img_obj.name.split('.')[1]
            img_name = "img_"+str(time.time())+"."+postfix
            img_path = os.path.join(settings.BASE_DIR, 'static', 'img', img_name)
            img_url = os.path.join(settings.SERVER_DIR, img_name)
            # 这里file_path是存储文件的路径
            # print(settings.BASE_DIR)
            with open(img_path, 'wb') as f:
                for chunk in img_obj.chunks():
                    f.write(chunk)
        except Exception:
            img_url = ""
        res = bottle_handler.add_bottle(uid,bookname, writer, press, des_path, img_url, timeouthandle, sendto)
        ust_handler.insert_star(uid, res["botid"], True)
        return HttpResponse(json.dumps({ "msg" : "ok" }), content_type="application/json")

def appendReceiveOrder(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        postBody = request.body
        json_result = json.loads(postBody)
        # todo: 查看该漂流瓶状态
        orres = order_hanler.append_receive_order(uid,json_result["expresscompany"],json_result["trackingnumber"],json_result["botid"],json_result["address"],json_result["name"],json_result["phonenumber"])
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg" : "fail to create order" }), content_type="application/json")
        res = bottle_handler.bind_order(json_result["botid"],orres["oid"])
        if res["state"]==1:
            return HttpResponse(json.dumps({ "msg" : "fail to bind order" }), content_type="application/json")
        return HttpResponse(json.dumps({ "msg" : "sucess", "oid":orres["oid"] }), content_type="application/json")

def completeOrder(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        orres = order_hanler.fill_sent_order(json_result["oid"], json_result["expresscompany"], json_result["trackingnumber"])
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg" : "fail" }), content_type="application/json")
        return HttpResponse(json.dumps({ "msg" : "success" }), content_type="application/json")

def retrieveBook(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        postBody = request.body
        json_result = json.loads(postBody)
        res = bottle_handler.get_bottle(json_result["botid"])
        if res["state"]==1:
            return HttpResponse(json.dumps({ "msg" : "fail to get bottle" }), content_type="application/json")
        if not (res["infos"][7]==0 and res["infos"][9]==3 and res["infos"][10]!=-1):
            return HttpResponse(json.dumps({ "msg" : "invalid operation" }), content_type="application/json")
        reoid = res["infos"][10]
        gores = order_hanler.get_order_with_oid(reoid)
        if(gores["state"]==1):
            return HttpResponse(json.dumps({ "msg" : "fail to get recieve order" }), content_type="application/json")
        orres = order_hanler.append_sent_order(-1,uid,json_result["botid"], orres["infos"]["address"], orres["infos"]["name"], orres["infos"]["phonenumber"])
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg" : "fail to append retrieve order" }), content_type="application/json")
        return HttpResponse(json.dumps({ "msg" : "success", "oid" : orres["oid"] }), content_type="application/json")

def getBookInfos(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        book = book_handler.get_book(json_result["bookname"], json_result["writer"], json_result["press"])
        if book["state"]==1:
            resp = {
                "msg" : "not exist"
            }
        else:
            resp = {
                "msg" : "success",
                'bookname': book["infos"][1],
                'writer': book["infos"][2],
                'press': book["infos"][3],
                'neededcredit': book["infos"][4],
                'coverurl': book["infos"][5],
                'description': book["infos"][6]
                }
        return HttpResponse(json.dumps(resp), content_type="application/json")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        res1 = user_handler.check_user_with_phonenumber(username, password);
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        if res1["state"]==0:
            request.session['uid'] = res1["uid"]
            print(session_id)
            resp = {
                "msg" : "success",
                "uid" : res1["uid"],
                "bottlenum" : bottle_handler.bottle_cnt(),
                "sessionid" : session_id,
                "issuper" : res1["issuper"]
            }
            cache.set(session_id,res1["uid"],2*60*60)
            return HttpResponse(json.dumps(resp), content_type="application/json")
        res2 = user_handler.check_user_with_username(username, password)
        if res2["state"]==0:
            request.session['uid'] = res2["uid"]
            print(session_id)
            resp = {
                "msg" : "success",
                "uid" : res2["uid"],
                "bottlenum" : bottle_handler.bottle_cnt(),
                "sessionid" : session_id,
                "issuper" : res2["issuper"]
            }
            cache.set(session_id,res2["uid"],2*60*60)
            return HttpResponse(json.dumps(resp), content_type="application/json")
        if res1["state"]==2 or res2["state"]==2:
            resp = {
                "msg" : "wrong password"
            }
            return HttpResponse(json.dumps(resp), content_type="application/json")
        resp = {
            "msg" : "no such user"
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")

def getBottleNum(request):
    if request.method == 'POST':
        res = {
            "msg" : "success",
            "bottlenum" : bottle_handler.bottle_cnt()
        }
        return HttpResponse(json.dumps(res), content_type="application/json")

def visBottle(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        bottlenum = bottle_handler.bottle_cnt()
        res = bottle_handler.vis_bottle(json_result["idx"])
        if res["state"]==0:
            try:
                file_object = open(res["infos"][4])
                file_context = file_object.read()
                resp = {
                    "msg" : "success",
                    "botid" : res["infos"][0],
                    "bookname" : res["infos"][1],
                    "writer" : res["infos"][2],
                    "press" : res["infos"][3],
                    "description" : file_context,
                    "photourls" : res["infos"][5],
                    "ispicked" : (res["infos"][7]!=0),
                    "isdonated" : (res["infos"][7]!=-1),
                    "donateTo" : (res["infos"][7] if res["infos"][7]<0 else 1),
                    "uploaddatetime" : res["infos"][8].strftime("%Y-%m-%d %H:%M:%S"),
                    "state" : res["infos"][9]
                }
            finally:
                file_object.close()
            return HttpResponse(json.dumps(resp), content_type="application/json")
        resp = {
            "msg" : "not exist"
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")

def getBottle(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        bottlenum = bottle_handler.bottle_cnt()
        res = bottle_handler.get_bottle(json_result["botid"])
        if res["state"]==0:
            try:
                file_object = open(res["infos"][4])
                file_context = file_object.read()
                resp = {
                    "msg" : "success",
                    "bookname" : res["infos"][1],
                    "writer" : res["infos"][2],
                    "press" : res["infos"][3],
                    "description" : file_context,
                    "photourls" : res["infos"][5],
                    "ispicked" : (res["infos"][7]!=0),
                    "isdonated" : (res["infos"][7]!=-1),
                    "donateTo" : (res["infos"][7] if res["infos"][7]<0 else 1),
                    "uploaddatetime" : res["infos"][8].strftime("%Y-%m-%d %H:%M:%S"),
                    "state" : res["infos"][9]
                }
            finally:
                file_object.close()
            return HttpResponse(json.dumps(resp), content_type="application/json")
        resp = {
            "msg" : "not exist"
        }
        return HttpResponse(json.dumps(resp), content_type="application/json")

def getStarInfos(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        res = ust_handler.select_stars_table(uid)
        return HttpResponse(json.dumps(res), content_type="application/json")

def getUserInfos(request):
    if request.method == 'POST':
        print(request.META.get("HTTP_AUTHORIZATION"))
        print("upupup")
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        res = user_handler.get_user_infos(uid)
        if res["state"]==0:
            resp = {
                "msg" : "success",
                "username" : res["infos"][0],
                "phonenumber" : res["infos"][1],
                "address" : res["infos"][2],
                "credit" : res["infos"][3],
                "enrolldatetime" : res["infos"][4].strftime("%Y-%m-%d %H:%M:%S"),
                "issuper" : res["infos"][5],
                "uid" : res["infos"][6]
            }
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {
                "msg" : "not exist"
            }
            return HttpResponse(json.dumps(resp), content_type="application/json")

def removeStar(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        postBody = request.body
        json_result = json.loads(postBody)
        ust_handler.remove_star(uid,json_result["bid"])
        return HttpResponse(json.dumps({ "msg":"success" }), content_type="application/json")

def writeOffAccount(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        postBody = request.body
        json_result = json.loads(postBody)
        res = user_handler.del_user(uid)
        if res["state"]==0:
            return HttpResponse(json.dumps({ "msg":"success" }), content_type="application/json")
        else:
            return HttpResponse(json.dumps({ "msg":"fail" }), content_type="application/json")

def addStar(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        postBody = request.body
        json_result = json.loads(postBody)
        ust_handler.insert_star(uid,json_result["bid"],False)
        return HttpResponse(json.dumps({ "msg":"success" }), content_type="application/json")

def pickBook(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        postBody = request.body
        json_result = json.loads(postBody)
        
        bottle_res = bottle_handler.get_bottle(json_result["botid"]);
        name = json_result["address"]["name"]
        phonenumber = json_result["address"]["phonenumber"]
        address = json_result["address"]["province"]+"-"+json_result["address"]["city"]+"-"+json_result["address"]["district"]+"-"+json_result["address"]["specific"]
        if bottle_res["state"]==1:
            return HttpResponse(json.dumps({ "msg":"bottle not exist" }), content_type="application/json")
        bookname = bottle_res["infos"][1]
        writer = bottle_res["infos"][2]
        press = bottle_res["infos"][3]

        book_res = book_handler.get_book(bookname, writer, press)
        if book_res["state"]==1:    # 书目信息不存在
            return HttpResponse(json.dumps({ "msg":"book not exist" }), content_type="application/json")
        neededcredit = book_res["infos"][4]

        bures = bottle_handler.before_update_sendto(json_result["botid"], uid)
        if bures["state"]==2:    # 书本不是可领取状态
            return HttpResponse(json.dumps({ "msg":"invalid operation" }), content_type="application/json")
        
        res = user_handler.increase_credit(uid, -neededcredit)
        if res["state"]==1:    # 操作用户不存在
            return HttpResponse(json.dumps({ "msg":"user not exist" }), content_type="application/json")
        if res["state"]==2:    # 积分不足
            return HttpResponse(json.dumps({ "msg":"not enought credit" }), content_type="application/json")
        
        orres = order_hanler.append_sent_order(1,uid,json_result["botid"],address,name,phonenumber)
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg":"fail to append order" }), content_type="application/json")

        bottle_handler.update_sendto(json_result["botid"], uid, orres["oid"])

        return HttpResponse(json.dumps({ "msg":"success", "oid":orres["oid"] }), content_type="application/json")
        
def updateAddress(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        postBody = request.body
        json_result = json.loads(postBody)
        res = user_handler.update_address(uid, json_result["new_address"]);
        if(res["state"]==1):return HttpResponse(json.dumps({ "msg":"fail" }), content_type="application/json")
        return HttpResponse(json.dumps({ "msg":"success" }), content_type="application/json")

def getAllOrders(request):
    if request.method == 'POST':
        res = order_hanler.get_all_order()
        if(res["state"]==1):return HttpResponse(json.dumps({ "msg":"fail" }), content_type="application/json")
        return HttpResponse(json.dumps({ "msg":"success", "orders":res["orders"] }), content_type="application/json")

def rejectOrder(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        orres = order_hanler.get_order_with_oid(json_result["oid"])
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg":"fail to get order"}), content_type="application/json")
        order_hanler.update_state(json_result["oid"])
        res = bottle_handler.update_state(orres["infos"]["botid"], 3)
        if res["state"]==1:
            return HttpResponse(json.dumps({ "msg":"fail to update state"}), content_type="application/json")
        return HttpResponse(json.dumps({ "msg":"success"}), content_type="application/json")

def acceptOrder(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        orres = order_hanler.get_order_with_oid(json_result["oid"])
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg":"fail to get order"}), content_type="application/json")
        order_hanler.update_state(json_result["oid"])
        res = bottle_handler.update_state(orres["infos"]["botid"], 2)
        if res["state"]==1:
            return HttpResponse(json.dumps({ "msg":"fail to update state"}), content_type="application/json")
        return HttpResponse(json.dumps({ "msg":"success"}), content_type="application/json")

def getOrder(request):
    if request.method == 'POST':
        postBody = request.body
        json_result = json.loads(postBody)
        orres = order_hanler.get_order_with_oid(json_result["oid"])
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg":"fail to get order"}), content_type="application/json")
        return HttpResponse(json.dumps({
            "msg" : "success",
            "infos" : orres["infos"]
        }), content_type="application/json")
        
def getOrdersOfUser(request):
    if request.method == 'POST':
        try:
            uid = cache.get(request.META.get("HTTP_AUTHORIZATION"));
            if not uid: raise Exception();
        except Exception:
            return HttpResponse(json.dumps({ "msg":"invalid" }), content_type="application/json")
        orres = order_hanler.get_order_with_uid(uid)
        if orres["state"]==1:
            return HttpResponse(json.dumps({ "msg":"fail to get order"}), content_type="application/json")
        return HttpResponse(json.dumps({
            "msg" : "success",
            "orders" : orres["orders"]
        }), content_type="application/json")