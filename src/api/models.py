from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    """
    Function creates an empty UserInfo attached to the created User if Slack_ID
    isn't provided upon User creation
    """
    if created:
        try:
            instance.userinfo
        except UserInfo.DoesNotExist:
            UserInfo.objects.create(user=instance)
