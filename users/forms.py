from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        error_messages={'required': '请输入用户名'}
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱'}),
        error_messages={'required': '请输入邮箱', 'invalid': '邮箱格式不正确'}
    )
    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
        min_length=6,
        error_messages={'required': '请输入密码'}
    )
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认密码'}),
        min_length=6,
        error_messages={'required': '请再次输入密码'}
    )
    captcha = forms.CharField(
        label='验证码',
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入验证码'}),
        error_messages={'required': '请输入验证码'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('两次密码不一致')
        return p2

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        error_messages={'required': '请输入用户名'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
        error_messages={'required': '请输入密码'}
    )
    captcha = forms.CharField(
        label='验证码',
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入验证码'}),
        error_messages={'required': '请输入验证码'}
    )

class ResetPasswordForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        error_messages={'required': '请输入用户名'}
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱'}),
        error_messages={'required': '请输入邮箱', 'invalid': '邮箱格式不正确'}
    )
    password1 = forms.CharField(
        label='新密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新密码'}),
        min_length=6,
        error_messages={'required': '请输入新密码'}
    )
    password2 = forms.CharField(
        label='确认新密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认新密码'}),
        min_length=6,
        error_messages={'required': '请再次输入新密码'}
    )
    captcha = forms.CharField(
        label='验证码',
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入验证码'}),
        error_messages={'required': '请输入验证码'}
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('两次密码不一致')
        return cleaned