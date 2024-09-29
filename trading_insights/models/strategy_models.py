from django.db import models
from django.utils.translation import gettext_lazy as _

from trading_insights.models.raw_data_models import (
    Account
 )


class Scenario(models.Model):

    class Meta:
        verbose_name = _("Scenario")
        verbose_name_plural = _("Scenarios")

    name = models.CharField(_("Name"), null=False, blank=False)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ScenarioLine(models.Model):

    class Meta:
        verbose_name = _("Scenario Line")
        verbose_name_plural = _("Scenario Lines")

    scenario = models.ForeignKey(
        Scenario, null=False, blank=False, on_delete=models.PROTECT,
        related_name="lines"
    )
    start_date = models.DateField(_("Start Date"), null=False, blank=False)
    end_date = models.DateField(_("End Date"), null=False, blank=False)
    start_amount = models.DecimalField(_("Start Amount"), max_digits=15, decimal_places=2)
    target_amount = models.DecimalField(_("Target Amount"), max_digits=15, decimal_places=2)
    daily_profit_ratio = models.DecimalField(
        _("Daily Target Profit"), max_digits=5, decimal_places=2, null=False, blank=False
    )
    weekly_withdrawal_amount = models.DecimalField(
        _("Weekly Withdrawal Amount"), max_digits=13, decimal_places=2, null=False, blank=False
    )

    def __str__(self):
        return f"{self.scenario.name} - {self.start_date.strftime('%d/%m/%y')}"
