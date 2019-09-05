from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('login', views.login_view, name='login'),

    path('register', views.register_view, name='register'),

    path('logout', views.logout_view, name='logout'),

    path('records', views.records_view, name='records'),

    path('upload', views.upload_view, name='upload'),

    path('delete', views.delete_view, name='delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)