from django.urls import path
from .views import home, signIn, signUp, signOut

urlpatterns = [
    path('', home, name='home'),
    path('signin', signIn, name='signin'),
    path('signup', signUp, name='signup'),
    path('signout', signOut, name='signout')
]