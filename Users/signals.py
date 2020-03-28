from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from Users.models import UserExt


@receiver(signal=post_save, sender=User)
def create_userext_after_user(sender, instance: User, created, **kwargs):
    if not created:
        return
    UserExt.objects.create(user=instance)


@receiver(signal=post_save, sender=User)
def save_userext_after_user(sender, instance: User, created, **kwargs):
    if created:
        return
    instance.userext.save()
