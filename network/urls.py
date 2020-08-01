
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:uid>", views.profileView, name="profileView"),
    path("following",views.followingView,name="followingView"),
    
    #API
    path("Edit/<int:id>", views.editpost, name="editpost"),
    path("like/<int:id>", views.likepost, name="likepost"),
    path("follow/<str:username>",views.follow,name="follow")
    
]
