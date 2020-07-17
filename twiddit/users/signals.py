from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from account.models import Account


@receiver(signal=post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(signal=post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()