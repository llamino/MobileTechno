# accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

User = get_user_model()

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="نام")
    last_name = forms.CharField(max_length=30, required=False, label="نام خانوادگی")
    photo = forms.ImageField(required=False, label="عکس پروفایل")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="تایید رمز عبور")

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("رمز عبور و تایید آن مطابقت ندارند.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # استفاده از get_or_create به جای create
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': self.cleaned_data['first_name'],
                    'last_name': self.cleaned_data['last_name'],
                    'photo': self.cleaned_data.get('photo')
                }
            )
            if not created:
                # اگر پروفایل قبلاً وجود داشته باشد، آن را به‌روزرسانی کنید
                profile.first_name = self.cleaned_data['first_name']
                profile.last_name = self.cleaned_data['last_name']
                if self.cleaned_data.get('photo'):
                    profile.photo = self.cleaned_data.get('photo')
                profile.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="نام کاربری یا شماره تلفن", max_length=150)

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="رمز عبور فعلی", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="رمز عبور جدید", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="تایید رمز عبور جدید", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    """
    فرم برای ویرایش اطلاعات مدل User.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

class ProfileUpdateForm(forms.ModelForm):
    """
    فرم برای ویرایش اطلاعات مدل Profile.
    """
    first_name = forms.CharField(max_length=30, required=False, label="نام")
    last_name = forms.CharField(max_length=30, required=False, label="نام خانوادگی")
    photo = forms.ImageField(required=False, label="عکس پروفایل")
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'photo']


