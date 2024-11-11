from typing import Callable

import flet as ft

from xpense.types import Routes


def get_navigation_bar(navigator: Callable):
    return ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOUSE_ROUNDED, label=Routes.HOUSEHOLD.value),
            ft.NavigationBarDestination(icon=ft.icons.CALENDAR_MONTH, label=Routes.CALENDAR.value),
            ft.NavigationBarDestination(
                icon=ft.icons.QUERY_STATS,
                selected_icon=ft.icons.QUERY_STATS,
                label=Routes.STATISTICS.value,
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.SETTINGS_ROUNDED,
                selected_icon=ft.icons.SETTINGS_ROUNDED,
                label=Routes.SETTINGS.value,
            ),
        ],
        selected_index=0,
        bgcolor=ft.colors.BLUE,
        bottom=True,
        on_change=navigator,
    )
