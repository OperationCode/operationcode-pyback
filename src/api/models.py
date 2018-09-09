from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    """
    Model used to extend Django's base User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slack_id = models.CharField(max_length=16)

    def __str__(self):
        return f'Username: {self.user} Slack ID: {self.slack_id}'


class Channel(models.Model):
    name = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=32)
    mods = models.ManyToManyField(UserInfo)

    def __str__(self):
        return f'{self.name} - {self.channel_id}'
