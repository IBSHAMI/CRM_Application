from django.db import models
from django.contrib.auth.models import AbstractUser


# we use abstract user model from django so we have more flexibility if we want to change the user model
class User(AbstractUser):
    pass


# create a database table that will hold the leads information
class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    # using ForeignKey we can create multiple leads for one agent
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Agents model
class Agent(models.Model):
    # we use OneToOneField to create one to one relationship with the User model
    # This way we can make sure that the agent is only one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# --------------------------- different types of models entries ----------------------------#
# # check if they have phone number
# Is_phone_number = models.BooleanField(default=False)
#
# # the source from which the lead came
# LEAD_SOURCES = (
#     ('Youtube', 'Youtube'),
#     ('Facebook', 'Facebook'),
#     ('Instagram', 'Instagram'),
#     ('Twitter', 'Twitter'),
#     ('Google', 'Google'),
#     ('Other', 'Other'),
# )
# lead_source = models.CharField(choices=LEAD_SOURCES, max_length=50)
# profile_image = models.ImageField(blank=True, null=True)
# additional_files = models.FileField(blank=True, null=True)
