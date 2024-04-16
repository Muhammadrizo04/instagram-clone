from directs.views import *
from django.urls import path

urlpatterns = [
    path('', inbox, name="message"),
    path('direct/<username>', Directs, name="directs"),
    path('send/', SendDirect, name="send-directs"),
    path('search/', UserSearch, name="search-users"),
    path('new/<username>', NewConversation, name="conversation"),
    path('delete_chat/', delete_chat, name='delete_chat_url'),
    path('delete-message/<int:message_id>/', delete_message, name='delete_message'),


]