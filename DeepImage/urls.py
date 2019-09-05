from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('login', views.login_view, name='login'),

    path('register', views.register_view, name='register'),

    path('logout', views.logout_view, name='logout'),

    path('rocords', views.records_view, name='records'),

    path('upload', views.upload_view.as_view(), name='basic_upload'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)