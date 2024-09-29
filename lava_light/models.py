from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractUser, Group, Permission
)

from easy_thumbnails.fields import ThumbnailerImageField

from lava_light.utils import (
    Result, generate_password, get_user_photo_filename,
    get_model_fields
)


class BaseModel(models.Model):

    list_display_fields = [
        ("__str__", "__model_name__")
    ]
    cashed_list_display_fields = None
    readonly_fields = []
    menu_icon_class = "anticon anticon-select"

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        _("Created at"), null=True, blank=True, default=timezone.now
    )
    created_by = models.ForeignKey(
        "lava_light.User", on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    last_updated_at = models.DateTimeField(
        _("Last update"), null=True, blank=True, auto_now=True
    )
    deleted_at = models.DateTimeField(_("Deleted at"), null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        app_label = self._meta.app_label
        model_name = self._meta.model_name.lower()
        lava_light_app_label = "lava_light"
        return reverse(f'{lava_light_app_label}:{app_label}_{model_name}_detail', args=(self.pk,))

    def get_update_url(self):
        app_label = self._meta.app_label
        model_name = self._meta.model_name.lower()
        lava_light_app_label = "lava_light"
        return reverse(f'{lava_light_app_label}:{app_label}_{model_name}_update', args=(self.pk,))

    def create(self, user=None, *args, **kwargs):
        if self.id:
            return Result.error(_("L'objet %(obj_name)s est déjà créé." % {
                "obj_name": self._meta.verbose_name
            }))

        self.created_by = user
        self.save(*args, **kwargs)

        return Result.success(_("L'objet %(obj_name)s est créé avec succès." % {
            "obj_name": self._meta.verbose_name
        }))

    def update(self, user=None, update_fields=None, *args, **kwargs):
        if not self.id:
            return Result.error(_("L'objet %(obj_name)s n'est pas encore créé." % {
                "obj_name": self._meta.verbose_name
            }))

        self.save(update_fields=update_fields, *args, **kwargs)

        return Result.success(_("L'objet %(obj_name)s est modifié avec succès." % {
            "obj_name": self._meta.verbose_name
        }))

    def delete(self, user=None, *args, **kwargs):
        if not self.id:
            return Result.error(_("L'objet %(obj_name)s n'est pas encore créé." % {
                "obj_name": self._meta.verbose_name
            }))

        super().delete(*args, **kwargs)

        return Result.success(_("L'objet %(obj_name)s est supprimé avec succès." % {
            "obj_name": self._meta.verbose_name
        }))

    @classmethod
    def get_list_url(cls):
        app_label = cls._meta.app_label
        model_name = cls._meta.model_name.lower()
        lava_light_app_label = "lava_light"
        return reverse(f'{lava_light_app_label}:{app_label}_{model_name}_list')

    @classmethod
    def get_create_url(cls):
        app_label = cls._meta.app_label
        model_name = cls._meta.model_name.lower()
        lava_light_app_label = "lava_light"
        return reverse(f'{lava_light_app_label}:{app_label}_{model_name}_create')

    @classmethod
    def get_list_display(cls):
        if cls.cashed_list_display_fields:
            return cls.cashed_list_display_fields

        # @TODO: Support methods and properties
        # list_display_fields = [
        #   "id",
        #   ("get_full_name", _("Nom complet")),
        #   "age"
        # ]

        # all_fields = cls._meta.get_fields(include_parents=True)
        all_fields = get_model_fields(cls)
        display_fields = []
        if cls.list_display_fields:
            display_fields = list(filter(
                (lambda item : item.name in cls.list_display_fields), all_fields
            ))

        cls.cashed_list_display_fields = display_fields
        return display_fields


class User(BaseModel, AbstractUser):

    class Meta(AbstractUser.Meta):
        ordering = ("-date_joined", "last_name", "first_name")

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("Permissions d'utilisateur"),
        blank=True,
        help_text=_("Des permissions spécifique à cet utilisateur."),
        related_name="users",
        related_query_name="user",
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Groupes"),
        blank=True,
        help_text=_(
            # "The groups this user belongs to. A user will get all permissions "
            # "granted to each of their groups."
            "Les groupes où cet utilisateur appartiens. Un utilisateur prend systématiquement"
            "touts les droits de ces groupes."
        ),
        related_name="users",
        related_query_name="user",
    )

    photo = ThumbnailerImageField(
        _("Photo"), upload_to=get_user_photo_filename, blank=True, null=True
    )
    tmp_pwd = models.CharField(
        _("Temporary password"), max_length=64, default="", blank=True
    )

    def get_all_permissions(self):
        user_perms_ids = self.user_permissions.all().values_list("id", flat=True)
        groups_perms_ids = self.groups.all().values_list("permissions__id", flat=True)
        return Permission.objects.filter(pk__in=[*user_perms_ids, *groups_perms_ids])

    def create(
        self,
        user=None,
        groups=None,
        password=None,
        force_is_active=False,
        generate_tmp_password=False,
    ):
        if password is not None:
            result = self.validate_password(password)
            if not result.success:
                return result
        elif generate_tmp_password:
            password = generate_password(12)
            self.tmp_pwd = password

        if force_is_active:
            self.is_active = True

        if password:
            self.set_password(password)

        result = super().create(user=None)
        if result.is_error:
            return result

        if groups is not None:
            self.groups.set(groups)

        return Result.success(
            message=_("L'utilisateur est créé avec succès."),
            instance=self,
        )

    # def set_password(self, raw_password, user=None):
    #     self.password = make_password(raw_password)
    #     self._password = raw_password

    #     if not self.username:
    #         # We do this to fix an error where if the user is not found on login
    #         # Django calls User().set_password(rp) to increase request time span
    #         # for some reason?
    #         return super().set_password(raw_password)

    #     result = self.update(
    #         user=user, update_fields=["password"]
    #     )
    #     if result.is_error:
    #         return result
    #     return Result.success(_("Password has been changed successfully."))

    @classmethod
    def validate_password(cls, password):
        if not isinstance(password, str):
            return Result.error(message=_("`password` must be a string."))

        try:
            validate_password(password, User)
            return Result.success(message=_("User password is valid."))
        except ValidationError as e:
            return Result.error(message=_("Invalid password."), errors=e.messages)
