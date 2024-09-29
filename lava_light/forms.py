import importlib

from django.utils.translation import gettext_lazy as _
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


def try_import_form(model, model_form_suffix="Form"):

    try:
        app_label = model._meta.app_label
        model_name = model._meta.model.__name__
        forms_module = importlib.import_module(f"{app_label}.forms")
        CustomModelListView = getattr(
            forms_module, "%s%s" % (model_name, model_form_suffix)
        )
        return CustomModelListView
    except (ImportError, AttributeError) as e:
        return None


def get_model_form(model, fields=None, action=None):

    if fields is None:
        fields = [
            f.name for f in model._meta.local_fields if f.editable
        ]

    CustomForm = try_import_form(model, model_form_suffix="Form")
    if CustomForm:
        return CustomForm

    class GenericBaseModelForm(forms.ModelForm):
        class Meta:
            pass

        Meta.model = model
        Meta.fields = fields

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()

            model_name = model._meta.model_name.lower()
            self.helper.form_id = f"{model_name}_form"
            self.helper.form_class = f"{model_name}_form form col-sm-12 col-md-12 col-lg-8 form-horizontal"
            self.helper.form_method = "POST"
            self.helper.label_class = "col-lg-2"
            self.helper.field_class = "col-lg-10"
            if action and action == "update":
                self.helper.add_input(Submit("submit", _("Modifier")))
            elif action and action == "create":
                self.helper.add_input(Submit("submit", _("Ajouter")))

    return GenericBaseModelForm
