"""stydybud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import home,room,create_room,deleteRoom,topicPage,activityPage,settingsUser,userProfile,registerUser,logoutUser,updated_room,loginPage,deleteMessage
urlpatterns = [
    path('login',loginPage,name = 'loginPage'),
    
    path('register',registerUser,name = 'register'),
    path('logout',logoutUser,name = 'logoutUser'),
    path('',home,name='home'),
    path('room/<int:pk>',room,name='room'),
    path('profile/<str:pk>',userProfile,name='profile'),
    
    path('settings',settingsUser,name='settings'),
    path('create-room/',create_room,name='create-room'),
    path('updated-room/<int:pk>',updated_room,name='updated-room'),
    path('delete-room/<int:pk>',deleteRoom,name='delete-room'),
    
    path('delete-message/<int:pk>',deleteMessage,name='delete-message'),

    
    path('topics',topicPage,name='topic'),
    
    path('activitys',activityPage,name='activity'),
    
]

