from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', max_length=100)


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', max_length=100)
    again = forms.CharField(label='再输一次密码', max_length=100)
