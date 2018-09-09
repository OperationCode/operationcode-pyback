from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Channel, UserInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )


class ModsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            'id',
            'slack_id',
        )


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    mods = ModsSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Channel
        fields = '__all__'

    def create(self, validated_data):
        mods_data = validated_data.pop('mods')
        channel = Channel.objects.create(**validated_data)
        return channel


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserInfo
        fields = '__all__'

    def create(self, validated_data):
        user_data = {key: value for key, value in validated_data.pop('user').items() if value}
        user, created = User.objects.get_or_create(**user_data)
        userinfo = UserInfo.objects.create(**validated_data, user=user)

        return userinfo

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.slack_id = validated_data.get('slack_id', instance.slack_id)

        user = instance.user
        user.username = user_data.get('username', user.username)
        user.is_staff = user_data.get('is_staff', user.is_staff)
        user.email = user_data.get('email', user.email)

