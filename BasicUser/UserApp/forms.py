from django import forms
from django.contrib.auth.models import User
from UserApp.models import UserProfileInfo

# create form classes using forms.ModelForm
class UserForm(forms.ModelForm):

    # create a password field
    password = forms.CharField(widget=forms.PasswordInput())

    # create a meta class which connects the form with the model
    class Meta():

        # Set the model attribute to the actual user model of Django
        model = User

        # include the filed that are required from the model
        fields = ('username','email','password')


# create a class for the userdefined model
class UserProfileInfoForm(forms.ModelForm):
    
    class Meta():
        # set the model to the userdefined model
        model = UserProfileInfo
        # include the actual fields
        fields = ('portfolio_site','profile_pic')
