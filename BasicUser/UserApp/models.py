from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# create a class UserProfileInfo model
class UserProfileInfo(models.Model):

    # create a onetoone relation to the actual built-in user model of django, donot inherit directly!
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional classes that we need
    # create a portfolio field with attribute blank=true which means it should not be a problem if the field is blank
    portfolio_site = models.URLField(blank=True)

    # create a profile pic field where user can  upload their pic
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
