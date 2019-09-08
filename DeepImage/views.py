from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, PhotoForm
from .image import process
from .models import Record
import requests
import time
import datetime


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/DeepImage/upload')

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
                    u = User(username=form.cleaned_data['username'],
                             password=make_password(form.cleaned_data['password']))
                    u.save()
                    return HttpResponseRedirect('/DeepImage/login')
                else:
                    form.errors['username'] = '用户名已被使用'
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/DeepImage/login')


def records_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/DeepImage/login')
    if request.method == 'GET':
        if request.user.is_superuser:
            records = Record.objects.all()
        else:
            records = Record.objects.filter(username=request.user.username)
        from_date = datetime.datetime.strptime('2000-1-1', "%Y-%m-%d")
        to_date = datetime.datetime.strptime('2100-12-31', "%Y-%m-%d")
        if request.GET.get('from') is not None and request.GET.get('to') is not None:
            try:
                from_date = datetime.datetime.strptime(request.GET.get('from'), "%Y-%m-%d")
            except ValueError:
                pass

            try:
                to_date = datetime.datetime.strptime(request.GET.get('to'), "%Y-%m-%d")
            except ValueError:
                pass

        records = [rcd for rcd in records if from_date <=
                        datetime.datetime.strptime(rcd.time.split(' ')[0], "%Y-%m-%d") <= to_date]

        from_date = from_date.strftime('%Y-%m-%d')
        to_date = to_date.strftime('%Y-%m-%d')

        records_ = list(reversed(records))
        paginator = Paginator(records_, 8)
        page = request.GET.get('page')
        if page is None:
            page = 1
        records_ = paginator.get_page(page)
        print(from_date, to_date)
        return render(request, 'records.html', {'records': records_, 'page': page,
                                                'from': from_date, 'to': to_date})


def upload_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/DeepImage/login')

    if request.method == 'GET':
        return render(request, 'index.html')

    elif request.method == 'POST':
        data = {}
        print(request.content_type)
        if request.POST.get('fromurl') is None:
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save()
                output_url1 = 'static/media/out1_' + photo.file.name
                output_url2 = 'static/media/out2_' + photo.file.name
                process(photo.file.url, output_url1, output_url2)

                ts = int(time.time())
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                rcd = Record(username=request.user.username, original_url=photo.file.url,
                             processed_url1=output_url1, processed_url2=output_url2, time=dt)
                rcd.save()

                data = {'is_valid': True, 'url': photo.file.url,
                        'output_url1': output_url1, 'output_url2': output_url2}
            else:
                data = {'is_valid': False}
        else:
            url = request.POST.get('fileurl')
            if url is not None:
                try:
                    res = requests.get(url)
                    if res.status_code == 200:
                        filename = str(time.time()).replace('.','_') + '.' + url.split('.')[-1]
                        fileurl = 'static/media/' + filename
                        with open(fileurl, 'wb') as fp:
                            fp.write(res.content)
                            fp.close()
                            output_url1 = 'static/media/out1_' + filename
                            output_url2 = 'static/media/out2_' + filename
                            process('static/media/' + filename, output_url1, output_url2)

                            ts = int(time.time())
                            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                            rcd = Record(username=request.user.username, original_url=fileurl,
                                         processed_url1=output_url1, processed_url2=output_url2, time=dt)
                            rcd.save()

                            data = {'is_valid': True, 'url': fileurl,
                                    'output_url1': output_url1, 'output_url2': output_url2}

                    else:
                        print(res.status_code)
                        data = {'is_valid': False}
                except Exception as e:
                    data = {'is_valid': False}
        return JsonResponse(data)


def delete_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/DeepImage/login')

    if request.user.is_superuser:
        records = Record.objects.all()
    else:
        records = Record.objects.filter(username=request.user.username)

    from_date = datetime.datetime.strptime('2000-1-1', "%Y-%m-%d")
    to_date = datetime.datetime.strptime('2100-12-31', "%Y-%m-%d")
    if request.GET.get('from') is not None and request.GET.get('to') is not None:
        try:
            from_date = datetime.datetime.strptime(request.GET.get('from'), "%Y-%m-%d")
        except ValueError:
            pass

        try:
            to_date = datetime.datetime.strptime(request.GET.get('to'), "%Y-%m-%d")
        except ValueError:
            pass

    records = [rcd for rcd in records if from_date <=
               datetime.datetime.strptime(rcd.time.split(' ')[0], "%Y-%m-%d") <= to_date]

    if request.method == 'GET':
        records_ = list(reversed(records))
        paginator = Paginator(records_, 8)
        page = request.GET.get('page')
        if page is None:
            page = 1
        records_ = paginator.get_page(page)
        return render(request, 'delete.html', {'records': records_})

    if request.method == 'POST':
        del_list = request.POST.getlist('record')
        for rcd in records:
            if str(rcd.id) in del_list:
                rcd.delete()
        return HttpResponseRedirect('/DeepImage/records')


def redirect_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/DeepImage/login')
    return HttpResponseRedirect('/DeepImage/upload')
