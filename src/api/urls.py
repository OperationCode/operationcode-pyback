from rest_framework.routers import SimpleRouter
from django.urls import path

from . import views

router = SimpleRouter()
router.register('channels', views.ChannelViewSet)
router.register('users', views.UserViewSet)
router.register('userinfos', views.UserInfoViewSet)
router.register('mods', views.UserModsList)

urlpatterns = router.urls

urlpatterns += [
    path('botMessages', views.bot_messages, name='bot_messages'),
    path('deleteMessage/<str:channel>/<str:ts>', views.delete_message, name='delete_message'),
]
