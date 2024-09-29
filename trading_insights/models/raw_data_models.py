from django.db import models
from django.utils.translation import gettext_lazy as _

from trading_insights.settings import (
    POSITION_TYPE_CHOICES,
    SYMBOL_TYPE_CHOICES
)


class Symbol(models.Model):

    class Meta:
        verbose_name = _("Symbol")
        verbose_name_plural = _("Symbols")

    name = models.CharField(_("Symbol"), null=False, blank=False)
    display_name = models.CharField(_("Extended name"), default="", blank=True)
    symbol_type = models.CharField(_("Type"), choices=SYMBOL_TYPE_CHOICES, default="forex", blank=False)
    pip_value = models.DecimalField(
        _("Pip value"), default=0.0001,max_digits=6, decimal_places=4, blank=True
    )

    def __str__(self):
        if self.display_name:
            return f"{self.name} ({self.display_name})"
        return self.name


class Account(models.Model):

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    name = models.CharField(_("Account Name"), null=False, blank=False)
    broker = models.CharField(_("Broker"), default="", blank=True)
    account_id = models.CharField(_("Account ID"), default="", blank=True)
    starting_balance = models.DecimalField(
        _("Starting Balance"), default=0, max_digits=13, decimal_places=2, blank=True
    )

    def __str__(self):
        return self.name


class Position(models.Model):

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    account = models.ForeignKey(Account, null=False, blank=False, on_delete=models.PROTECT)
    symbol = models.ForeignKey(Symbol, null=False, blank=False, on_delete=models.PROTECT)
    position_id = models.CharField(_("Position ID"), default="", blank=True)
    position_type = models.CharField(
        _("Type"), choices=POSITION_TYPE_CHOICES, null=False, blank=False
    )

    open_time = models.DateTimeField(_("Open Time"), null=False, blank=False)
    close_time = models.DateTimeField(_("Open Time"), null=False, blank=False)
    volume = models.DecimalField(_("Volume"), max_digits=6, decimal_places=2)
    open_price = models.DecimalField(_("Open Price"), max_digits=10, decimal_places=5)
    stop_loss = models.DecimalField(_("Stop Loss"), max_digits=10, decimal_places=5)
    take_profit = models.DecimalField(_("Take Profit"), max_digits=10, decimal_places=5)
    close_price = models.DecimalField(_("Close Price"), max_digits=10, decimal_places=5)
    commission = models.DecimalField(_("Commission"), max_digits=6, decimal_places=2)
    swap = models.DecimalField(_("Swap"), max_digits=6, decimal_places=2)
    profit = models.DecimalField(_("Profit"), max_digits=13, decimal_places=2)
    amount = models.DecimalField(
        _("Amount"), default=0, max_digits=13, decimal_places=2, blank=True,
        help_text=_("Deposited or withdrawn amount.")
    )

    def __str__(self):
        amount = self.profit
        if self.position_type in ["deposit", "withdraw"]:
            amount = self.amount
        return f"{self.get_position_type_display()} - {amount} - {self.open_time.strftime('%d/%m/%Y %H:%M')}"
