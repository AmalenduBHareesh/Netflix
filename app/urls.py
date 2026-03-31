from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', userlogin, name='home'),
    path('signup/', signup, name='signup'),
    path('userlogin/', userlogin, name='userlogin'),
    path('logout/', userlogout, name='logout'),


    path('index/', index, name='index'),

    path('genre/<str:id>/', genre_view, name='genre'),
    path('mylist/', my_list, name='my_list'),
    path('search/', search, name='search'),
    path('add-to-list/', add_to_list, name='add_to_list'),
]