from django.http import HttpResponse

from UserModel.models import User

import json

import user_handler
import book_handler

import os

from django.conf import settings

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
        file_path = os.path.join(settings.BASE_DIR, 'static2', 'img', file_obj.name)
        # 这里file_path是存储文件的路径
        # print(settings.BASE_DIR)
 
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse('ok')