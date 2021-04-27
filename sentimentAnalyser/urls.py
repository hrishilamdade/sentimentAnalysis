from django.contrib import admin
from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url
urlpatterns = [
    path('sentiment-analyser',views.home,name="index"),
    path('',views.home,name="index"),
    path('mention',views.mention,name="mention"),
    path('response',views.response,name="response"),
]
