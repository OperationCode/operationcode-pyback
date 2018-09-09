from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('forms/codeschool', views.CodeschoolFormView.as_view(), name='codeschool_form'),
    path('bot/messages', views.BotMessagesView.as_view(), name='bot_messages'),
]
