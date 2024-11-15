import dataclasses
from datetime import datetime
import uuid
from typing import Callable, Self, Optional

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
    MONTHLY = "monthly"
    YEARLY = "yearly"
    WEEKLY = "weekly"

    @classmethod
    def get_aggregation_type(cls, type_str: str) -> Self:
        if not isinstance(type_str, str):
            return None

        for aggregation_type in DataAggregation:
            if aggregation_type.value.lower() == type_str.lower():
                return aggregation_type
        return None


class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"
    ALLOCATION = "allocation"

    @classmethod
    def get_transaction_type(cls, type_str: str) -> Self:
        if not isinstance(type_str, str):
            return None

        for transaction_type in TransactionType:
            if transaction_type.value.lower() == type_str.lower():
                return transaction_type
        return None


class Currency(Enum):
    RON = "ron"
    EURO = "euro"
    DOLLAR = "dollar"

    @classmethod
    def get_currency_type(cls, type_str: str) -> Self:
        if not isinstance(type_str, str):
            return None

        for currency in Currency:
            if currency.value.lower() == type_str.lower():
                return currency
        return None


def uuid4_factory() -> str:
    return str(uuid.uuid4())


@dataclasses.dataclass
class Transaction:
    type: Optional[TransactionType] = None
    date: Optional[datetime] = None
    amount: Optional[str] = None
    currency: Optional[Currency] = None
    category: Optional[str] = None
    id: Optional[str] = dataclasses.field(default_factory=uuid4_factory)


class TransactionOperations(Enum):
    ADD = "add"
    EDIT = "edit"
