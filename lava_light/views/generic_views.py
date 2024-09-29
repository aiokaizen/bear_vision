import importlib

from django.shortcuts import redirect
from django.views.generic import (
    DetailView as BaseDetailView,
    ListView as BaseListView,
    UpdateView as BaseUpdateView,
    CreateView as BaseCreateView,
    TemplateView, RedirectView
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from lava_light.utils import Result
from lava_light.forms import get_model_form


def try_import_view(model, model_view_suffix="View"):

    try:
        app_label = model._meta.app_label
        model_name = model._meta.model.__name__
        views_module = importlib.import_module(f"{app_label}.views")
        CustomModelListView = getattr(
            views_module, "%s%s" % (model_name, model_view_suffix)
        )
        return CustomModelListView
    except (ImportError, AttributeError) as e:
        return None


class BaseViewMixin:

    def get_template_names(self):
        """
        This method checks for template files in a specific order,
        Let's say you want to get the list template of your model `polls.Bar`.
        The order in which files are going to be retrieved is:
            1. polls/bar_list.html  # Model specific template file.
            2. polls/generics/list.html  # If you want to provide a shared list.html file
                between all models of an app.
            3. lava_light/generics/list.html  # The default file that is chosen if none of
                the above was found.
        """

        names = super().get_template_names()

        if hasattr(self, 'object_list'):
            if hasattr(self.object_list, 'model'):
                opts = self.object_list.model._meta
                template_name_suffix = self.template_name_suffix[1:]  # _list > list
                names.append("%s/generics/%s.html" % (opts.app_label, template_name_suffix))

            if self.generic_template_name:
                names.append(self.generic_template_name)
        return names


class ProtectedBaseViewMixin(BaseViewMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProtectedTemplateView(ProtectedBaseViewMixin, TemplateView):
    pass


class ProtectedRedirectView(ProtectedBaseViewMixin, RedirectView):
    pass


class BaseProtectedModelViewMixin(ProtectedBaseViewMixin):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["model_verbose_name"] = self.model._meta.verbose_name
        context["model_verbose_name_plural"] = self.model._meta.verbose_name_plural
        available_fields = self.model._meta.get_fields(include_parents=True)
        context["model_fields"] = available_fields
        context["list_url"] = self.model.get_list_url()
        context["create_url"] = self.model.get_create_url()
        return context


class ListView(BaseProtectedModelViewMixin, BaseListView):

    generic_template_name = "lava_light/generics/list.html"
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        available_fields = self.model._meta.get_fields(include_parents=True)
        if hasattr(self.model, "get_list_display"):
            available_fields = self.model.get_list_display()
        context["model_fields"] = available_fields
        context["view"] = "list"
        return context


class DetailView(BaseProtectedModelViewMixin, BaseDetailView):

    template_name = "lava_light/generics/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["view"] = "details"
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        if action == "delete":
            instance = self.get_object()
            result : Result = instance.delete()
            if result.is_success:
                messages.success(request, result.message)
            else:
                messages.error(request, result.message)

        return redirect(self.model.get_list_url())


class CreateView(BaseProtectedModelViewMixin, BaseCreateView):

    template_name = "lava_light/generics/form.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["view"] = "create"
        return context


class UpdateView(BaseProtectedModelViewMixin, BaseUpdateView):

    template_name = "lava_light/generics/form.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["view"] = "update"
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def get_list_view(model):

    # Check if the model has a custom view first
    CustomModelListView = try_import_view(model, "ListView")
    if CustomModelListView:
        return CustomModelListView

    # Otherwise, create a generic view
    class GenericListView(ListView):

        def __init__(self, **kwargs):
            self.model = model
            self.paginate_by = 20

            super().__init__()

    return GenericListView


def get_detail_view(model):

    form_class = get_model_form(model, fields=None)

    # Check if the model has a custom view first
    CustomModelDetailView = try_import_view(model, "DetailView")
    if CustomModelDetailView:
        return CustomModelDetailView

    class GenericDetailView(DetailView):

        def __init__(self, **kwargs):
            self.model = model
            self.form_class = form_class

            super().__init__()

    return GenericDetailView


def get_create_view(model):

    form_class = get_model_form(model, fields=None, action="create")

    # Check if the model has a custom view first
    CustomModelCreateView = try_import_view(model, "CreateView")
    if CustomModelCreateView:
        return CustomModelCreateView

    class GenericCreateView(CreateView):

        def __init__(self, **kwargs):
            self.model = model
            self.form_class = form_class

            super().__init__()

    return GenericCreateView


def get_update_view(model):

    form_class = get_model_form(model, fields=None, action="update")

    # Check if the model has a custom view first
    CustomModelUpdateView = try_import_view(model, "UpdateView")
    if CustomModelUpdateView:
        return CustomModelUpdateView

    class GenericUpdateView(UpdateView):

        def __init__(self, **kwargs):
            self.model = model
            self.form_class = form_class

            super().__init__()

    return GenericUpdateView
