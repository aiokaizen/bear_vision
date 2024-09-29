from django.shortcuts import redirect, render, reverse
from django.views.generic import (
    TemplateView,
    RedirectView
)
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordResetView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetCompleteView
)

from lava_light.views.generic_views import (
    ProtectedTemplateView, ProtectedRedirectView
)


class HomeView(ProtectedTemplateView):
    template_name = "lava_light/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["latest_articles"] = Article.objects.all()[:5]
        return context


class NotificationsView(ProtectedTemplateView):
    template_name = "lava_light/notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["latest_articles"] = Article.objects.all()[:5]
        context["model_verbose_name"] = "Notification"
        context["model_verbose_name_plural"] = "Notifications"
        return context


class SignupView(TemplateView):
    template_name = "lava_light/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(BaseLoginView):
    template_name = "lava_light/login.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)


class PasswordReset(PasswordResetView):

    template_name = "lava_light/pwd_reset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(BaseLogoutView):

    template_name = "lava_light/login.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
