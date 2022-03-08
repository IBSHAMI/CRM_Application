from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


# we use abstract user model from django so we have more flexibility if we want to change the user model
class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class Organization(models.Model):
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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', related_name='leads', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics/')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


#  handle each file upload and save
def handle_upload_follow_up(instance, filename):
    return f'leads_followups/lead_{instance.lead.pk}/{filename}'


class FollowUp(models.Model):
    # we use related name here so we can access the leads from the follow up
    # ex: lead.follow_ups.all() (which will fetch all the follow ups for that lead)
    lead = models.ForeignKey(Lead, related_name='followups', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to=handle_upload_follow_up)

    def __str__(self):
        return self.lead.first_name + ' ' + self.lead.last_name


# Agents model
class Agent(models.Model):
    # we use OneToOneField to create one to one relationship with the User model
    # This way we can make sure that the agent is only one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# list leads to different categories
class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # different categories are New, Contacted, Converted and Unconverted
    # default catagory is New

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, *args, **kwargs):
    # instance: the user instance name
    # created: boolean value that tells us if the user was created or not at the moment of signal sending
    # sender: the sender of the signal
    if created and not instance.is_agent:
        Organization.objects.create(user=instance)


# django is listening for the user model to send event (saved) then use the function to handle the event
post_save.connect(post_user_created_signal, sender=User)
