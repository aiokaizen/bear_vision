from django.urls import path, include
from django.apps import apps

from lava_light.views import (
    get_list_view, get_detail_view,
    get_update_view, get_create_view,
    HomeView, NotificationsView,
    SignupView, LoginView, LogoutView,
    PasswordReset
)
from lava_light import settings as light_settings

app_name = "lava_light"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('notifications', NotificationsView.as_view(), name='notifications'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('password_reset', PasswordReset.as_view(), name="password_reset"),
    path('logout', LogoutView.as_view(), name='logout'),
]


for model_name in light_settings.MAIN_MENU_ITEMS:
    model = apps.get_model(model_name)
    app_label = model._meta.app_label
    model_name = model._meta.model_name

    urlpatterns.extend([
        path(
            f'{app_label}/{model_name}/',
            get_list_view(model).as_view(), name=f'{app_label}_{model_name}_list'
        ),
        path(
            f'{app_label}/{model_name}/create/',
            get_create_view(model).as_view(), name=f'{app_label}_{model_name}_create'
        ),
        path(
            f'{app_label}/{model_name}/<int:pk>/',
            get_detail_view(model).as_view(), name=f'{app_label}_{model_name}_detail'
        ),
        path(
            f'{app_label}/{model_name}/<int:pk>/update/',
            get_update_view(model).as_view(), name=f'{app_label}_{model_name}_update'
        ),
    ])
