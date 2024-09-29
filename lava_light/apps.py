from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LavaLightConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lava_light"
    verbose_name = _("Administration")
