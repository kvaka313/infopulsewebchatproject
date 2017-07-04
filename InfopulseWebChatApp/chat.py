import json

import sockjs.tornado
from django.contrib.sessions.models import Session
from redis.sentinel import Sentinel

from InfopulseWebChat.settings import SENTINEL_CONNECTION
from InfopulseWebChatApp.services import MessageService


class SocketHandler(sockjs.tornado.SockJSConnection):
    active_clients={}
    active_sessions={}

    def on_open(self, request):
        print("connection open")

    def on_close(self):
        print("connection was closed")

    def on_message(self, message):
        json_message=json.loads(message)
        if(json_message.get("sessionid")!=None):
           session_db=Session.objects.filter(session_key=\
                json_message.get("sessionid"))\
               .first()
           if (session_db==None):
               answer={}
               answer["auth"]="no"
               self.send(json.dumps(answer))

           login=None
           if(session_db!=None):
               session=session_db.get_decoded()
               login=session.get("login")

           if(login!=None):
               SocketHandler.active_clients[login]=self
               SocketHandler.active_sessions[login]=json_message.get("sessionid")
               messages=MessageService.get_all_messages_by_login(login)
               for message in messages:
                   answer={}
                   message_array=message.split(":")
                   answer["auth"]="yes"
                   answer["name"]=message_array[0]
                   answer["message"]=message_array[1]
                   self.send(json.dumps(answer))

               self.send_user_list()

           else:
               answer = {}
               answer["auth"] = "no"
               self.send(json.dumps(answer))

        elif(json_message.get("broadcast")!=None):
            login=self.get_login()
            if(login!=None):
                answer={}
                answer["name"]=login
                answer["message"]=json_message.get("broadcast")
                MessageService.save_broadcast_message(login,json_message.get("broadcast"))
                for socket in SocketHandler.active_clients.values():
                    socket.send(json.dumps(answer))
            else:
                answer = {}
                answer["auth"] = "no"
                self.send(json.dumps(answer))

        elif(json_message.get("name")!=None):
            login=self.get_login()
            if(login!=None):
                name=json_message.get("name")
                sock=SocketHandler.active_clients.get(name)
                if(sock!=None):
                    answer={}
                    answer["name"]=login
                    answer["message"]=json_message.get("message")
                    sock.send(json.dumps(answer))
                else:
                    MessageService.save_private_message(login,name,json_message.get("message"))

            else:
                answer = {}
                answer["auth"] = "no"
                self.send(json.dumps(answer))

        elif(json_message.get("logout")!=None):
            login = self.get_login()
            if (login != None):
                del SocketHandler.active_clients[login]
                sessionid=SocketHandler.active_sessions[login]
                del SocketHandler.active_sessions[login]
                self.invalidate_session(sessionid)
                self.send_user_list()
            else:
                answer = {}
                answer["auth"] = "no"
                self.send(json.dumps(answer))

    def send_user_list(self):
        users=SocketHandler.active_clients.keys()
        answer={"list":[]}
        for user in users:
            answer["list"].append(user)

        for socket in SocketHandler.active_clients.values():
            socket.send(json.dumps(answer))

    def invalidate_session(self,sessionid):
        Session.objects.filter(session_key=sessionid).first().delete()

    def get_login(self):
        for key,value in SocketHandler.active_clients.items():
            if(value==self):
                return key
        return None



















