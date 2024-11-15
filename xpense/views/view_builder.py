from typing import Optional

import flet as ft
import flet_route

from xpense.views.calendar.controls import get_calendar_controls
from xpense.views.household.household_controls import get_household_controls
from xpense.types import flet_route_callable_type, Routes


def get_view(route_url: str, controls: Optional[list[ft.Control]] = None) -> flet_route_callable_type:
    def get_main_view(page: ft.Page, params: flet_route.Params, basket: flet_route.Basket) -> ft.View:
        return ft.View(
            route=route_url,
            controls=controls,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor=ft.colors.WHITE70,
            spacing=0,
            padding=0,
        )

    return get_main_view
