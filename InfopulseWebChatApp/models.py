from django.db import models
class Role(models.Model):
    role_name=models.CharField(max_length=20)


class ChatUser(models.Model):
    name=models.CharField(max_length=30)
    login=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    role_id=models.ForeignKey(Role,on_delete=models.CASCADE)

class Message(models.Model):
    body=models.CharField(max_length=500)
    sender_id = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name="sender")
    receiver_id=models.ForeignKey(ChatUser,on_delete=models.CASCADE, related_name="receiver")


class Ban(models.Model):
    sender_id=models.OneToOneField(ChatUser)




