from typing import Callable, Self

import flet as ft
import flet_route
from enum import Enum

flet_route_callable_type = Callable[[ft.Page, flet_route.Params, flet_route.Basket], ft.View]


class Routes(Enum):
    HOUSEHOLD = "Household"
    CALENDAR = "Calendar"
    STATISTICS = "Statistics"
    SETTINGS = "Settings"
    ADD = "Add"

    @property
    def index(self):
        return list(Routes).index(self)


class DataAggregation(Enum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    WEEKLY = "WEEKLY"


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ALLOCATION = "allocation"

    @classmethod
    def get_transaction_type(cls, type_str: str) -> Self:
        if not isinstance(type_str, str):
            return None

        for transaction_type in TransactionType:
            if transaction_type.value.lower() == type_str.lower():
                return transaction_type
        return None
