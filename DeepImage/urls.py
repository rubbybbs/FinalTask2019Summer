from django.urls import path

from . import views

urlpatterns = [

    path('login', views.login_view, name='login'),

    path('register', views.register_view, name='register'),

    path('upload', views.BasicUploadView.as_view(), name='basic_upload')
]