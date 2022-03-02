from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


# we use abstract user model from django so we have more flexibility if we want to change the user model
class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# create a database table that will hold the leads information
class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    # using ForeignKey we can create multiple leads for one agent
    # set agent default to null so we can assign it later
    organization = models.ForeignKey(organization, on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Agents model
class Agent(models.Model):
    # we use OneToOneField to create one to one relationship with the User model
    # This way we can make sure that the agent is only one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def post_user_created_signal(sender, instance, created, *args, **kwargs):
    # instance: the user instance name
    # created: boolean value that tells us if the user was created or not at the moment of signal sending
    # sender: the sender of the signal
    if created:
        organization.objects.create(user=instance)


# django is listening for the user model to send event (saved) then use the function to handle the event
post_save.connect(post_user_created_signal, sender=User)
