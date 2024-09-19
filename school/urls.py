from django import views
from django.urls import path, re_path
from .views import *
from . import views

urlpatterns = [

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('room/<str:pk>/', views.room, name='room'),

    path('home/', views.home, name='hom'),
    path('', SchoolHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', Addpage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<slug:year_slug>/', show_category, name='category')
]
