from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .services import get_messages, delete
from .serializers import ChannelSerializer, UserSerializer, UserInfoSerializer
from .models import Channel, UserInfo


class ChannelViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserInfoViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer
    queryset = UserInfo.objects.all().select_related('user')


class UserModsList(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()

    def get_queryset(self):
        user_slack_id = self.request.query_params.get('slack_id', None)
        user_channel_id = self.request.query_params.get('channel_id', None)
        if user_slack_id:
            return Channel.objects.filter(mods__slack_id=user_slack_id, channel_id=user_channel_id).all()
        return self.queryset


def bot_messages(request):
    return JsonResponse({'data': get_messages()})


def delete_message(request, ts: str, channel: str):
    return JsonResponse(delete(ts, channel))
