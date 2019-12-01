from django.http import HttpResponse

from UserModel.models import User

import json

import user_handler
import book_handler

import os

from django.conf import settings

def addBook(request):
    if(request.method == 'POST'):
        print("the POST method")
        #concat = request.POST
        postBody = request.body
        # print(concat)
        # print(type(postBody))
        # print(postBody)
        json_result = json.loads(postBody)
        # print(json_result)
        book_handler.add_book(json_result["bookname"], json_result["writer"], json_result["press"], json_result["neededcredit"])
        return HttpResponse("<p>数据添加成功！</p>")

def addUser(request):
    if(request.method == 'POST'):
        print("the POST method")
        #concat = request.POST
        postBody = request.body
        # print(concat)
        # print(type(postBody))
        # print(postBody)
        json_result = json.loads(postBody)
        # print(json_result)
        user_handler.add_user(json_result["username"], json_result["password"], json_result["phonenumber"])
        return HttpResponse("<p>数据添加成功！</p>")

def delUser(request):
    uploader.upload_ajax(request)
#     print(book_handler.del_book("a","a","a")["state"])
#     return HttpResponse("<p>数据删除成功！</p>")

def upload(request):
 
    # name = request.POST()
    # return HttpResponse('ok')
#     if request.method == 'GET':
#         return render(request, 'upload.html')
#     else:
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
        postBody = request.body
        json_result = json.loads(postBody)
        res1 = user_handler.check_user_with_phonenumber(json_result["username"],json_result["password"]);
        if res1["state"]==0:
            resp = {
                "msg" : "success",
                "uid" : res1["uid"]
            }
            return HttpResponse(json.dumps(resp), content_type="application/json")
        res2 = user_handler.check_user_with_username(json_result["username"],json_result["password"])
        if res2["state"]==0:
            resp = {
                "msg" : "success",
                "uid" : res2["uid"]
            }
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
