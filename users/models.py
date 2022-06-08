from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # primary=True 를 User 의 PK로 설정하여 통합적으로 관리한다.
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=128, null=True)
    position = models.CharField(max_length=128, null=True)
    subjects = models.CharField(max_length=128, null=True)
    image = models.ImageField(upload_to="profile/", default="default.png")
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        