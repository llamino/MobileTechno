# accounts/views.py
from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm, CustomPasswordChangeForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View

# API Views

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Web Views



class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = form.save()

        # تنظیم backend برای کاربر
        user.backend = 'accounts.backends.UsernameOrPhoneBackend'

        # ورود کاربر
        login(self.request, user)

        # تولید توکن‌های JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # تنظیم توکن‌ها در کوکی‌ها
        response = super().form_valid(form)
        response.set_cookie(
            'access_token',
            access_token,
            httponly=True,
            secure=not self.request.is_secure(),
            samesite='Lax'
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=not self.request.is_secure(),
            samesite='Lax'
        )
        messages.success(self.request, 'ثبت نام با موفقیت انجام شد.')
        return response

class CustomLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        # Authenticate the user
        user = form.get_user()
        login(self.request, user)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Set tokens in cookies
        response = super().form_valid(form)
        response.set_cookie(
            'access_token',
            access_token,
            httponly=True,
            secure=not self.request.is_secure(),
            samesite='Lax'
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=not self.request.is_secure(),
            samesite='Lax'
        )
        messages.success(self.request, 'خوش آمدید!')
        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        messages.success(request, 'با موفقیت خارج شدید.')
        return response


class ProfileView(LoginRequiredMixin, View):
    """
    نما برای نمایش پروفایل کاربر.
    """
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class EditProfileView(LoginRequiredMixin, View):
    """
    نما برای ویرایش پروفایل کاربر.
    """
    template_name = 'accounts/edit_profile.html'

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت به‌روزرسانی شد.')
            return redirect('accounts:profile')

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)
class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/change_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('accounts:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # حفظ نشست کاربر بعد از تغییر رمز

        # Generate new JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Set new tokens in cookies
        response = super().form_valid(form)
        response.set_cookie(
            'access_token',
            access_token,
            httponly=True,
            secure=not self.request.is_secure(),
            samesite='Lax'
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=not self.request.is_secure(),
            samesite='Lax'
        )

        messages.success(self.request, 'رمز عبور با موفقیت تغییر یافت.')
        return response
