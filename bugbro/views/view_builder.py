from typing import Optional

import flet as ft
import flet_route

from bugbro.views.calendar.controls import get_calendar_controls
from bugbro.views.household.controls import get_household_controls
from bugbro.types import flet_route_callable_type, Routes


def get_view(route_url: str, controls: Optional[list[ft.Control]] = None) -> flet_route_callable_type:
    def get_main_view(page: ft.Page, params: flet_route.Params, basket: flet_route.Basket) -> ft.View:
        return ft.View(
            route=route_url,
            controls=controls,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    return get_main_view
