from lava_light.views.generic_views import (
    DetailView,
    UpdateView,
    CreateView,
    TemplateView
)

from lava_light.views import (
    ListView
)

from trading_insights.models import (
    Scenario, ScenarioLine
)


class ScenarioListView(ListView):

    model = Scenario

    def get(self, request, *args, **kwargs):
        # raise Exception("HI THERE FROM CUSTOM LIST VIEW")
        return super().get(request, *args, **kwargs)
