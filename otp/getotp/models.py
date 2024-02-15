import random
import string
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        app_label = 'getotp'
    # groups = models.ManyToManyField(Group, related_name='user_groups')
    # user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateTimeField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


class OtpRequest(models.Model):
    class OtpChannel(models.TextChoices):
        ANDROID = 'Android', _('Android')
        IOS = 'iOS', _('iOS')
        WEB = 'Web', _('Web')

    request_id = models.UUIDField(default=uuid.uuid4, editable=False)
    channel = models.CharField(_("Channel"), max_length=50, choices=OtpChannel.choices)
    phone = models.CharField(max_length=14)
    password = models.CharField(max_length=4, null=True)
    valid_from = models.DateTimeField(default=timezone.now())
    valid_until = models.DateTimeField(default=timezone.now() + timedelta(seconds=120))
    receipt_id = models.CharField(null=True, max_length=255)

    def generate_password(self):
        self.password = self.random_password()
        self.valid_until = timezone.now() + timedelta(seconds=120)

    def random_password(self):
        rand = random.SystemRandom()
        digits = rand.choices(string.digits, k=4)
        return ''.join(digits)

    class Meta:
        verbose_name = _('one time password')
        verbose_name_plural = _('one time passwords')
