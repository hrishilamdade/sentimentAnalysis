from django.contrib import admin
from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url
urlpatterns = [
    path('sentiment-analyser',views.home,name="index"),
    path('mention',views.mention,name="mention"),
    path('response',views.response,name="response"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
