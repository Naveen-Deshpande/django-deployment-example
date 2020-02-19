from django.urls import path
from UserApp import views

# set up the app name to use the template tagging
app_name = 'UserApp'

  # create URL patterns
urlpatterns = [
    path('registration/',views.registration,name='registration'),
    path('user_login/',views.user_login,name='user_login')
]
