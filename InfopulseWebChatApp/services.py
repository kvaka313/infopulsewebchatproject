from redis.sentinel import Sentinel

from InfopulseWebChat.settings import SENTINEL_CONNECTION
from InfopulseWebChatApp.models import ChatUser, Ban

class MessageService:
    sentinel = Sentinel([(SENTINEL_CONNECTION, 17777)], socket_timeout=0.1)
    database = sentinel.master_for('mymaster', socket_timeout=0.1)

    @staticmethod
    def get_all_messages_by_login(login):
        pass

    @staticmethod
    def save_broadcast_message(sender, message):
        pass

    @staticmethod
    def save_private_message(sender, receiver, message):
        pass



class ChatUserService:
    @staticmethod
    def save_user(user_form):
       if user_form.is_valid():
            user_name=user_form.cleaned_data["name"]
            user_login=user_form.cleaned_data["login"]
            user_password=user_form.cleaned_data["password"]
            chat_user=ChatUser(name=user_name,login=user_login,password=user_password,role_id_id=1)
            try:
              chat_user.save()
              return True
            except ValueError:
              return False
       else:
           return False

    @staticmethod
    def verify_credentials(userlogin,userpassword):
        chat_user = ChatUser.objects.filter(login=userlogin,password=userpassword).first()
        #select * from chat_users where login=userlogin and password=userpassword
        if(chat_user==None):
            return None
        return chat_user

    @staticmethod
    def ban_verify(user):
       ban =Ban.objects.filter(sender_id=user).first()
       if(ban!=None):
           return True
       else:
           return False


