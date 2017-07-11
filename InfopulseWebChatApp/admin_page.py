from django.core.serializers import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.urls import reverse
import json

from InfopulseWebChatApp.models import ChatUser, Ban


@api_view(['GET'])
def get_all_users(request):
    if (request.session.get('login') != None and request.session.get('is_admin') == True):
        all_users = ChatUser.objects.filter(role_id_id=1)
        json_users = {"users": []}
        for user in all_users:
            temp = {}
            b = Ban.objects.filter(sender_id=user).first()
            if b==None:
                temp["login"]=user.login
                temp["rel"]="add"
                temp["href"]=reverse("add_user")
                json_users["users"].append(temp)
            else:
                temp["login"]=user.login
                temp["rel"]="remove"
                print(b.id)
                temp["href"]=reverse("del_user",b.id)
                json_users["users"].append(temp)
            return HttpResponse(json.dumps(json_users), content_type='application/json', status=status.HTTP_200_OK)
    else:
        return HttpResponse("error login", status=400)

@csrf_exempt
@api_view(['GET','POST'])
def add_user_to_ban(request):
    if (request.session.get('login') != None and request.session.get('is_admin') == True):
            json_data = JSONParser().parse(request)
            user_login = json_data['login']
            u = ChatUser.objects.filter(login=user_login).first()
            b = Ban(sender_id=u)
            b.save()
            return HttpResponse("ok", status=status.HTTP_200_OK)
    else:
            return HttpResponse("error login", status=400)



@api_view(['DELETE'])
def delete_user_from_ban(request,ban_id):
    if (request.session.get('login') != None and request.session.get('is_admin') == True):
        u = Ban.objects.filter(id=ban_id).first()
        u.delete()
        return HttpResponse("ok", status=200)
    else:
        return HttpResponse("error login", status=400)



