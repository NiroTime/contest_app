from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from tasks.models import Task


class ImageField(models.ImageField):

    def save_form_data(self, instance, data):
        if data is not None:
            file = getattr(instance, self.attname)
            if file != data:
                file.delete(save=False)
        super(ImageField, self).save_form_data(instance, data)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    avatar = ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    rating = models.IntegerField(default=0, editable=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class UserActions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions',
    )
    description = models.TextField()
    action_url = models.CharField(max_length=250)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_create']


class UsersSolvedTasks(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='UST',
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='UST',
    )
    solved = models.BooleanField(default=False)
    decision = models.TextField(null=True, blank=True)
