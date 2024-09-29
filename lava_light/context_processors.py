from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.apps import apps

from lava_light import settings as light_settings


# Cashing support for menu items
CASHED_MAIN_MENU = list()


def get_menu_items():

    global CASHED_MAIN_MENU

    if CASHED_MAIN_MENU:
        return CASHED_MAIN_MENU

    model_list = []
    for model_name in light_settings.MAIN_MENU_ITEMS:
        model = apps.get_model(model_name)
        model_list.append(model)

    main_menu = [{
        "title": _("Tableau de bord"),
        "icon": "anticon anticon-dashboard",
        "url": reverse("lava_light:home"),
    }]

    for model in model_list:
        main_menu.append({
            "title": model._meta.verbose_name,
            "icon": model.menu_icon_class,
            "url": model.get_list_url()
        })

    CASHED_MAIN_MENU = main_menu

    return main_menu


def generics(request):
    context = {
        "main_menu": get_menu_items()
    }
    return context
