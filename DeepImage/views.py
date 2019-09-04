from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from .image import process

from .forms import PhotoForm
from .models import Photo
from django.http import JsonResponse
from django.views import View

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/DeepImage/upload')
            else:
                form.errors['password'] = '用户名或密码不正确'
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['again']:
                form.errors['again'] = '两次输入不一致'
            else:
                try:
                    u = User.objects.get(username=form.cleaned_data['username'])
                except User.DoesNotExist:
                    u = User(username=form.cleaned_data['username'], password=make_password(form.cleaned_data['password']))
                    u.save()
                    return HttpResponseRedirect('/DeepImage/login')
                else:
                    form.errors['username'] = '用户名已被使用'
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)


class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def upload_view(request):
    pass


