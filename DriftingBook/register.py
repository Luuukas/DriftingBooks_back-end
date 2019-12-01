import json
import user_handler
from django.http import HttpResponse
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.cache import cache
from django.utils.crypto import get_random_string


# get response from Aliyun api
def send_sms(PhoneNumbers,params):
    client = AcsClient('LTAI4Fj5nqYvrdqzgcMX1ZRD', 'cKCQBQmkxmrkWglblt7PmnDc3ofK53', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', PhoneNumbers)
    request.add_query_param('SignName', "漂流图书")
    request.add_query_param('TemplateCode', "SMS_179225017")

    request.add_query_param('TemplateParam', params)

    response = client.do_action(request)
    print(str(response, encoding = 'utf-8'))
    return response


def sms_state_handler(response):
    code = json.loads(response)['Code']
    if code != "OK":
        return {"code":0 ,"message":"验证码发送失败"}
    return {"code":1,"message":"success"}


# 调用该函数发送sms并将PhoneNumbers和code存入cache中
def send_sms_view(request):
    code = get_random_string(length=4, allowed_chars="0123456789")
    params = "{\"code\":\"" + code + "\"}"
    tele = str(request.GET.get('PhoneNumbers'))
    sms_result = sms_state_handler(send_sms(tele,params))

    if sms_result["code"] == 1:
        cache.set(tele, code, timeout=600)
    return HttpResponse(json.dumps(sms_result, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")


# input:
# json:
# {
#     username:XXX
#     password:XXX
#     phonenumber:XXX
#     code:XXX
# }

# output
# success
# {
#     "state":1
# }

# failure
# {
#     "state":0
# }
def register(request):
    if(request.method == "POST"):
        result = json.loads(request.body)
        username = result["username"]
        password = result["password"]
        phonenumber = result["phonenumber"]
        code = result["code"]

        # check if phonenumber corresponds to code
        if code != cache.get(phonenumber):
            result = {"code":0,"message":"验证码错误"}
            return HttpResponse(json.dumps(result,ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        r1 = user_handler.check_user_with_phonenumber(phonenumber, "")
        # phonenumber existed
        if r1['state'] != 1:
            result = {"code":0,"message":"手机号已被注册"}
            return HttpResponse(json.dumps(result,ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        r2 = user_handler.check_user_with_username(username, "")
        # username existed
        if r2['state'] != 1:
            result = {'code':0,"message":"用户名已被注册"}
            return HttpResponse(json.dumps(result,ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        # success
        user_handler.add_user(username,password,phonenumber)
        result = {'code':1,"message":"success"}
        return HttpResponse(json.dumps(result,ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

