from django.conf import settings


LOCKED_PERMISSIONS = getattr(settings, "LOCKED_PERMISSIONS", {
    "models": [

    ],
    "permissions": [

    ],
})

MAIN_MENU_ITEMS = getattr(settings, "MAIN_MENU_ITEMS", [])
