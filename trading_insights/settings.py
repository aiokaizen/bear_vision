from django.utils.translation import gettext_lazy as _


POSITION_TYPE_CHOICES = (
    ("buy", _("Buy")),
    ("sell", _("Sell")),
    ("deposit", _("Deposit")),
    ("withdraw", _("Withdraw")),
)


SYMBOL_TYPE_CHOICES = (
    ("forex", _("Forex")),
    ("commodity", _("Commodity")),
    ("stock", _("Stock"))
)


SYMBOLS = [
    "EURUSD", "GBPUSD", "USDCHF", "USDJPY", "USDCAD", "AUDUSD",
    "AUDCAD", "AUDCHF", "AUDJPY", "CHFJPY", "EURGBP", "EURAUD",
    "EURCHF", "EURJPY", "EURCAD", "GBPCHF", "GBPJPY", "CADCHF",
    "CADJPY", "GBPAUD", "GBPCAD", "AUDNZD", "EURNZD", "AUDSGD",
    "CHFSGD", "EURDKK", "EURHKD", "EURNOK", "EURPLN", "EURSEK",
    "EURSGD", "EURTRY", "EURZAR", "GBPDKK", "GBPNOK", "GBPSEK",
    "GBPSGD", "GBPTRY", "NOKJPY", "NOKSEK", "SEKJPY", "SGDJPY",
    "USDCNH", "USDCZK", "USDDKK", "USDHKD",
 ]
