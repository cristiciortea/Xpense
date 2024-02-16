from typing import Callable

import flet as ft


def get_header_current_day_button(current_day: int, func: Callable) -> ft.TextButton:
    return ft.TextButton(
        width=35,
        height=35,
        content=ft.Container(
            content=ft.Column([ft.Text(str(current_day), size=10, color=ft.colors.BLACK)],
                              alignment=ft.MainAxisAlignment.CENTER,
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,

        ),
        style=ft.ButtonStyle(
            shape=ft.BeveledRectangleBorder(radius=13),
            color=ft.colors.BLACK,
            bgcolor=ft.colors.TRANSPARENT,
            surface_tint_color=ft.colors.BLACK,
            side=ft.BorderSide(width=2, color=ft.colors.BLACK26)
        ),
        on_click=func,
    )


def get_header_calendar_icon() -> ft.Container:
    return ft.Container(
        width=32,
        height=32,
        alignment=ft.alignment.center,
        content=ft.Icon(
            name=ft.icons.CALENDAR_MONTH_SHARP,
            size=15,
            opacity=0.65
        )
    )
