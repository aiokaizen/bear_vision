import os
from django.utils.text import slugify


SUCCESS_TAG_NAME = "success"
ERROR_TAG_NAME   = "error"
WARNING_TAG_NAME = "warning"


def slugify(value, separator="_", allow_unicode=False):
    result = base_slugify(value, allow_unicode).replace("-", separator)
    return result


def get_model_fields(model):
    options = model._meta
    # fields = {}
    # for field in sorted(options.concrete_fields + options.many_to_many + options.virtual_fields):
    #     fields[field.name] = field
    # return fields
    # fields = sorted(options.concrete_fields + options.many_to_many + options.virtual_fields)
    fields = model._meta.get_fields(include_parents=True)
    return fields


class immutable_dict(dict):
    """Immutable dictionary."""

    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError("This object is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class Result(immutable_dict):
    """
    An immutable Result object representing
    both Success and Error results from functions and APIs.
    """

    def __init__(
        self,
        tag: str = SUCCESS_TAG_NAME,
        message: str = "",
        instance: any = None,
        errors: dict = None,
        error_code: str = "",
    ):
        self.tag = tag
        self.message = message
        self.instance = instance
        self.errors = errors
        self.error_code = error_code

        self.is_success = True if self.tag == SUCCESS_TAG_NAME else False
        self.is_error = True if self.tag == ERROR_TAG_NAME else False
        self.is_warning = True if self.tag == WARNING_TAG_NAME else False

        dict.__init__(
            self,
            is_success=self.is_success,
            is_error=self.is_error,
            is_warning=self.is_warning,
            message=message,
            errors=errors,
            error_code=self.error_code,
        )

    @classmethod
    def success(self, message="", instance=None):
        return Result(
            tag=SUCCESS_TAG_NAME, message=message, instance=instance
        )

    @classmethod
    def warning(self, message="", instance=None, error_code=""):
        return Result(
            tag=WARNING_TAG_NAME,
            message=message,
            instance=instance,
            error_code=error_code,
        )

    @classmethod
    def error(self, message="", instance=None, errors=None, error_code=""):
        return Result(
            tag=ERROR_TAG_NAME, message=message, instance=instance,
            errors=errors, error_code=error_code
        )

    def to_dict(self):

        res_dict = {
            "class_name": "lava_light.utils.Result",
            "result": self.tag,
            "message": str(self.message),
        }

        if not self.is_success:
            res_dict["errors"] = self.errors or []
            res_dict["error_code"] = self.error_code
        if self.instance:
            if hasattr(self.instance, 'id'):
                res_dict["object_id"] = self.instance.id
            elif type(self.instance) in (dict, list, tuple, int, str, float, chr):
                res_dict["object"] = self.instance
            else:
                res_dict["object"] = str(self.instance)

        return res_dict


def generate_password(length=8, include_special_characters=True):
    lower_alphabets = "abcdefghijklmnopqrstuvwxyz"
    upper_alphabets = lower_alphabets.upper()
    numbers = "1234567890"
    special_characters = "-_!?.^*@#$%"
    pool = lower_alphabets + upper_alphabets + numbers
    if include_special_characters:
        pool += special_characters

    random_password = "".join(random.SystemRandom().choices(pool, k=length))
    return random_password


def get_user_photo_filename(instance, filename):
    filename, ext = os.path.splitext(filename)
    return "user/{filename}{}".format(slugify(filename), ext)
