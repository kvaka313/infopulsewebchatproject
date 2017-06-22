from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from InfopulseWebChatApp.forms import RegistrationForm
from InfopulseWebChatApp.models import ChatUser
from InfopulseWebChatApp.services import ChatUserService
from InfopulseWebChatApp.validators import CredentialsValidator


class RegistrationController(FormView):
    template_name = "registration.html"
    form_class = RegistrationForm
    def post(self,request):
        reg_form=RegistrationForm(request.POST)
        if ChatUserService.save_user(reg_form):
          root_url=reverse("index")
          return redirect(root_url)
        else:
           return render(request,"registration.html",{"form":reg_form})



class LoginController(View):
    def get(self,request):
       return render(request,"login.html",{})

    def post(self,request):
        if(request.session.get("error")!=None):
            del request.session["error"]
            login_url=reverse("login")
            return redirect(login_url)
        user_login=request.POST["userlogin"]
        user_password=request.POST["userpassword"]
        #todo validation
        if(not CredentialsValidator.login_password_validation(user_login) or not CredentialsValidator.login_password_validation(user_password)):
          request.session["error"]="not valid"
          return render(request,"login.html",{"error":"not valid"})

        user=ChatUserService.verify_credentials(user_login,user_password)
        if(user!=None and user.role_id.role_name=="user"):
           if(ChatUserService.ban_verify(user)):
               request.session["login"]=user.login
               request.session["is_admin"]=False
               request.session["is_banned"]=True
               ban_url=reverse("ban")
               return redirect(ban_url)
           else:
               request.session["login"] = user.login
               request.session["is_admin"] = False
               request.session["is_banned"] = False
               chat_url = reverse("chat")
               return redirect(chat_url)


        if (user != None and user.role_id.role_name == "admin"):
            request.session["login"] = user.login
            request.session["is_admin"] = True
            admin_url = reverse("admin")
            return redirect(admin_url)
        request.session["error"] = "Login incorrect"
        return render(request,"login.html",{"error":"login incorrect"})

class IndexController(View):
    def get(self,request):
        registartion_url=reverse("registration")
        login_url=reverse("login")
        return render(request,"index.html",{"login_url":login_url,"registration_url":registartion_url})

class AdminController(View):
    def get(self,request):
        pass

class ChatController(View):
    def get(self,request):
        pass

class BanController(View):
    def get(self,request):
        return render(request,"ban.html",{})

