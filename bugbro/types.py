from typing import Callable

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
