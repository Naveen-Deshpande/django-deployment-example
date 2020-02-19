from django.shortcuts import render
from UserApp.forms import UserForm, UserProfileInfoForm

# imports to use the django built-in modules for login/logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.

# home page view
def index(request):
    return render(request,'UserApp/index.html')


# logout view after login
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# simple view which requires login
@login_required
def special(request):
    return HttpResponse('You are logged in, so only you can view this message')


# Registration view
def registration(request):

    # check if user is registered or not
    # we need to pass this variable in the dictionary to the registration.html
    registered = False

    # check if the the user has posted back through the registeration page
    if request.method == 'POST':

        # create a variable matching to the forms in forms.py
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if both the forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # save the data directly to the database
            user = user_form.save()
            # set the password hashing for the entered password
            user.set_password(user.password)
            # save the data to the database
            user.save()

            # save the data from profile form to the database without committing
            profile = profile_form.save(commit=False)

            # link the profile data to the user with one to one relation in views.
            # models.py-> user(created one to one relation with USER)
            # user -> is the user form, which originally is defined in forms.py with model = User
            # model, form, view all three are interconnected in this way
            profile.user = user

            # check if the user has uploaded a profile pic using the request.FILES modules.
            # this applies for all other file types also
            if 'profile_pic' in request.FILES:
                # request.FILES is a dictionary here and prfoile_pic is the key defined in the model
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            # after everything set registered variable true to indicate user is registered
            registered = True

            # else print the errors, either user_form is invalid or profile_form is invalid
        else:

            print(user_form.errors,profile_form.errors)

        # else if the user didn't post anything, we set up the actual registration form
    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'UserApp/registration.html',{'user_form':user_form,
                                                        'profile_form':profile_form,
                                                        'registered':registered})



# login view for users to login
def user_login(request):

    # check if the user has entered the login details
    if request.method == 'POST':

        # Grab the entered username and password
        # get method is used as simple form is used for login in login.html
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the entered details using built in django authenticate method
        user = authenticate(username=username, password=password)

        # if the user is authenticated, user is available
        if user:

            # check is the user active
            if user.is_active:

                # login the user with the entered details using builtin login module
                login(request,user)

                # Once logged in, redirect to home page
                return HttpResponseRedirect(reverse('index'))

                # if user account is not active, resturn a simple HttpResponse
            else:
                return HttpResponse('Your account is not active')

        else:
            # if the user is invalid or has entered invalid details
            print("Someone tried to login with invalid details")
            print("Username:{}, Password:{}".format(username,password))
            return HttpResponse("Invalid Credentials, Please try again!")

    else:
        # if the user has not entered the login details
        return render(request,'UserApp/login.html',{})
