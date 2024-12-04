from django.urls import path
from . import views

urlpatterns = [
    path("api/chat/history/", views.history, name="chat_history"),
    path("api/chat/send/", views.chatbot, name="chat_send"),
]
