from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatList.as_view(), name="index"),
    path('search/', views.AddDuoChatView.as_view(), name='search_user'),
    path('start-chat/', views.AddDuoChatView.as_view(), name='start_chat'),
    path('api/get_past_messages/<uuid:chat_id>/<uuid:message_id>/', views.get_past_messages, name='get_past_messages'),
    path("<str:room_name>/", views.room, name="room"),
]
