from celery import shared_task
from django.core.mail import send_mail
from .models import User
from chat_proj import settings


@shared_task
def send_code_via_email(id, addr="code@zraux.com"):
    try:
        user = User.objects.get(pk=id)
        subject = f'Your Confirmation Code'
        message = f"Hello {user.username},\n\nYour confirmation code is {user.confirm_code}.\n\nThank you for registering!"
        
        
        from_email = addr
        recipient_list = [user.email]

        # if DEBUG is `False` send_mail works
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        ) if not settings.DEBIG else print(message)
    
    except User.DoesNotExist:
        pass
    
   
        
    
    