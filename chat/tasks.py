# tasks.py
from celery import shared_task
from .models import DuoMessage, DuoChat
from accounts.models import User

@shared_task
def save_messages_in_db(user_id, room_name, message):
    """
    Save the chat message to the database.
    
    Args:
        user_id (int): ID of the user sending the message.
        room_name (str): Name of the chat room.
        message (str): The message content.
    """
    try:
        user = User.objects.get(id=user_id)
        chat = DuoChat.objects.get(pk=room_name)
        DuoMessage.objects.create(chat=chat, user=user, text=message)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        pass
    except DuoChat.DoesNotExist:
        # Handle the case where the chat room does not exist
        pass
