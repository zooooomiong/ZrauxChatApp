from django.shortcuts import render, redirect
from .models import DuoChat, DuoMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from accounts.models import User
from django.views import View

def index(request):
    return render(request, "index.html")

@login_required
def room(request, room_name):
    chat_room = DuoChat.objects.get(id=room_name)
    messages = DuoMessage.objects.filter(chat=chat_room).order_by('-created_at')[:15][::-1]
    return render(request, "room.html", {"room_name": room_name, "messages": messages})

@login_required
def get_past_messages(request, chat_id, message_id):
    message = DuoMessage.objects.get(id=message_id)
    messages = DuoMessage.objects.filter(chat_id=chat_id, created_at__lt=message.created_at).order_by('-created_at')[:10]
    response_data = {
        'messages': [{'id': msg.id, 'user': msg.user.username, 'text': msg.text} for msg in messages]
    }
    return JsonResponse(response_data)



class ChatList(LoginRequiredMixin, ListView):
    model = DuoChat
    template_name = "chats.html"
    context_object_name = "chats"
    
    def get_queryset(self):
        return self.request.user.chats.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chats = context['chats']
        other_users_dict = {}

        for chat in chats:
            other_user = chat.users.exclude(id=self.request.user.id).first()
            other_users_dict[chat.id] = other_user
            chat.user = other_user

        context['other_users_dict'] = other_users_dict
        return context

class ContactListView(View, LoginRequiredMixin):
    def get(self, request):
        # Get all users except the logged-in user
        contacts = User.objects.exclude(id=request.user.id).values('id', 'username')
        return JsonResponse(list(contacts), safe=False)


class AddDuoChatView(View, LoginRequiredMixin):
    
    def get(self, request):
        s = request.GET.get("s")
        user = None
        if s:
            try:
                user = User.objects.get(username=s)
                return JsonResponse({'user': {'id': user.id, 'username': user.username}})
            except User.DoesNotExist:
                return JsonResponse({'user': None})  # User not found
        return JsonResponse({'user': None})

    def post(self, request):
        user_id = request.POST.get("user_id", None)
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                
                # Check if the DuoChat already exists between the two users
                existing_chat = DuoChat.objects.filter(users=request.user).filter(users=user)
                if existing_chat.exists():
                    return JsonResponse({'success': False, 'message': 'Chat already exists.'})

                # Create a new chat if it doesn't exist
                dChat = DuoChat.objects.create()
                dChat.users.set([request.user, user])
                dChat.save()

                return JsonResponse({'success': True, 'message': 'Chat started.'})  # Indicate success
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found.'})

        return JsonResponse({'success': False, 'message': 'Invalid request.'})
    

    
    