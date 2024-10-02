from django.db import models
from accounts.models import User
from uuid import uuid4

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
   

class DuoChat(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    users = models.ManyToManyField(User, related_name="chats")

    def __str__(self) -> str:
        return f"{self.id}"
    def save(self, *args, **kwargs):
        
        
        super().save(*args, **kwargs)
                
                

class DuoMessage(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    chat = models.ForeignKey(DuoChat, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_message")
    text = models.TextField()