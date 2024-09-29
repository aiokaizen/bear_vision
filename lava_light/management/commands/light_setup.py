import logging

from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from lava_light.models import User, Group
from lava_light import settings as light_settings


class Command(BaseCommand):
    help = """
        This command should only be called once on the start of each
        project that includes lava_light app.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-logs",
            action="store_true",
            help="If this argument is set, the function will not print anything to the console.",
        )
        parser.add_argument(
            "--reset-users",
            action="store_true",
            help="If this argument is set, all users will be removed and recreated (This action is irreversible!!).",
        )
        parser.add_argument(
            "--reset-perms",
            action="store_true",
            help="If this argument is set, all permissions will be removed and recreated (This action is irreversible!!).",
        )

    def handle(self, *args, **options):
        no_logs = options["no_logs"]
        reset_perms = options["reset_perms"]
        reset_users = options["reset_users"]

        # Reset permissions:
        if reset_perms:
            logging.info("Resetting all permissions")
            Permission.objects.all().delete()
        # from django.utils import translation
        # translation.activate('fr')
        # print("current lang:", translation.get_language())

        # Create base model default permissions
        for model in apps.get_models():
            opts = model._meta
            content_type = ContentType.objects.get_for_model(model)

            model_full_name = f"{content_type.app_label}.{model.__name__.lower()}"
            if model_full_name in light_settings.LOCKED_PERMISSIONS["models"]:
                print("skipping model permissions for:", model_full_name)
                continue

            if hasattr(model, "_create_default_permissions"):
                default_permissions = model._create_default_permissions()
                for code_name, verbose_name in default_permissions:

                    permission_name = f"{content_type.app_label}.{code_name}"
                    if (
                        permission_name
                        in light_settings.LOCKED_PERMISSIONS["permissions"]
                    ):
                        print("Skipping permission:", permission_name)
                        continue

                    Permission.objects.get_or_create(
                        codename=code_name,
                        content_type=content_type,
                        defaults={
                            "name": verbose_name,
                        },
                    )
            else:
                # Create other models default permissions
                for perm in opts.default_permissions:
                    codename = f"{perm}_{opts.model_name}"
                    name = f"Can {perm} {opts.verbose_name}"

                    permission_name = f"{content_type.app_label}.{codename}"
                    if (
                        permission_name
                        in light_settings.LOCKED_PERMISSIONS["permissions"]
                    ):
                        print("Skipping permission:", permission_name)
                        continue

                    Permission.objects.get_or_create(
                        codename=codename,
                        content_type=content_type,
                        defaults={"name": name},
                    )

            # Create other permissions (From Meta.permissions)
            for perm in opts.permissions:
                codename = perm[0]
                name = perm[1]

                permission_name = f"{content_type.app_label}.{codename}"
                if permission_name in light_settings.LOCKED_PERMISSIONS["permissions"]:
                    print("Skipping permission:", permission_name)
                    continue

                Permission.objects.get_or_create(
                    codename=codename,
                    content_type=content_type,
                    defaults={"name": name},
                )

        # Create the group 'ADMINS' if it does not exist
        admins_group, _created = Group.objects.get_or_create(
            name="ADMINISTRATOR",
            # defaults={"is_system": True, "slug": "admins"}
        )
        # Group.objects.get_or_create(
        #     name="STANDARD", is_system=True
        # )  # Default group for signed up users

        # Add all available permissions to group ADMINS
        admins_group.permissions.add(
            *Permission.objects.all().values_list("id", flat=True)
        )

        # Reset users
        if reset_users:
            User.objects.all().delete()

        # Create the superuser and the admin users if they don't exist
        try:
            superuser = User.objects.get(username="superuser")
            logging.warning("superuser already exists!")
        except User.DoesNotExist:
            superuser = User(
                username="superuser",
                email="mouadkommir@gmail.com",
                first_name="Super",
                last_name="User",
                is_staff=True,
                is_superuser=True,
            )
            superuser.create(
                groups=[admins_group],
                password="admin_super_1234",
                force_is_active=True,
            )
            logging.info("superuser was created successfully!")

        try:
            admin = User.objects.get(username="admin")
            admin.groups.add(admins_group)
            logging.warning("admin user admin already exists!")
        except User.DoesNotExist:
            admin = User(
                username="admin",
                email="mouadkommir@gmail.com",
                first_name="System",
                last_name="Administrator",
                is_staff=True,
            )
            admin.create(
                groups=[admins_group],
                password="admin_1234",
                force_is_active=True,
            )
            logging.info("admin was created successfully!")
