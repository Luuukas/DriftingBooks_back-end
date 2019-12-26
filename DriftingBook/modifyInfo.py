from DriftingBook import register
import user_handler
import json
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.core.cache import cache

# 全局变量及共用的函数
responseTable = ["success",
                 "无法根据uid找到相关信息",
                 "密码错误",
                 "验证码错误"]

def constructHttpResponse(errorNum):
    resCode = 1 if errorNum == 0 else 0
    resMsg = responseTable[errorNum]
    response = {'code': resCode, "message": resMsg}
    return HttpResponse(json.dumps(response, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")


################################################################
#   以下为业务逻辑
################################################################

# 接收前端发来的uid(get请求)，向该用户名绑定的手机号发送短信验证码
def sendSms2BindedPhone(request):
    # uid是否需要转换为int?
    uid = int(request.GET.get('uid'))
    # get binded phonenumber from uid
    result = user_handler.get_phonenumber(uid)
    if result["state"] == 1:
        ret = "\"code\":0,\"message\":\"无法获取该用户绑定的手机号\""
        return HttpResponse(json.dumps(ret, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

    phonenumber = result["phonenumber"]
    code = get_random_string(length=4, allowed_chars="0123456789")
    params = "{\"code\":\"" + code + "\"}"
    sms_result = register.sms_state_handler(register.send_sms(phonenumber,params))

    if sms_result["code"] == 1:
        cache.set(phonenumber, code, timeout=600)
    return HttpResponse(json.dumps(sms_result, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")


# 接收uid、原密码、新密码与验证码
# input:
# (json)
# {
#   uid:XXX
#   oldpassword:XXX
#   newpassword:XXX
#   code:XXX
# }
def changePassword(request):
    if request.method == "POST":
        errorNum = 0
        result = json.loads(request.body)
        uid = result["uid"]
        oldpassword = result["oldpassword"]
        newpassword = result["newpassword"]
        code = result["code"]

        # check if old password correct
        userInfo = user_handler.get_user_infos(uid)
        if userInfo["state"]==0:
            #global errorNum
            passwordState = user_handler.check_user_with_username(userInfo["infos"][0],oldpassword)["state"]
            if passwordState == 1:
                errorNum = 1
            if passwordState == 2:
                errorNum = 2
        else:
            errorNum = 1

        # check if code correct
        if errorNum == 0 and code != cache.get(userInfo["infos"][1]):
            errorNum = 3

        # update password in database
        if errorNum == 0:
            user_handler.update_password(uid,newpassword)

        # according to errorNum
        # return 'Response' to front-end
        return constructHttpResponse(errorNum)


# input:
# {
#   uid:XXXX
#   password:XXXX
#   newphonenumber:XXXX
#   code:XXXX
# }
def changePhonenumber(request):
    if request.method == "POST":
        errorNum = 0
        result = json.loads(request.body)
        uid = result["uid"]
        password = result["password"]
        newphonenumber = result["newphonenumber"]
        code = result["code"]

        # check password
        userInfo = user_handler.get_user_infos(uid)
        if userInfo["state"]==0:
            passwordState = user_handler.check_user_with_username(userInfo["infos"][0],password)["state"]
            if passwordState == 1:
                #global errorNum
                errorNum = 1
            if passwordState == 2:
                errorNum = 2
        else:
            errorNum = 1

        # check code
        if errorNum == 0 and code != cache.get(newphonenumber):
            errorNum = 3

        # update phonenumber in database
        if errorNum == 0:
            user_handler.update_phonenumber(uid,newphonenumber)
        return constructHttpResponse(errorNum)




