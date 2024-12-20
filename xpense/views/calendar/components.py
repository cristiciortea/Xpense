import datetime
from typing import Callable

import flet as ft


def get_header_current_day_button(current_day: int, func: Callable) -> ft.TextButton:
    return ft.TextButton(
        width=37,
        height=35,
        content=ft.Container(
            content=ft.Column([ft.Text(str(current_day), size=10, color=ft.colors.BLACK)],
                              alignment=ft.MainAxisAlignment.CENTER,
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,

        ),
        style=ft.ButtonStyle(
            shape=ft.StadiumBorder(),
            color=ft.colors.BLUE_200,
            bgcolor=ft.colors.TRANSPARENT,
            surface_tint_color=ft.colors.BLUE_200,
            side=ft.BorderSide(width=2, color=ft.colors.BLUE_GREY_200)
        ),
        on_click=func,
    )


def get_header_calendar_icon(page: ft.Page, on_date_change: Callable[[datetime.datetime], None]) -> ft.Container:
    date_picker = ft.DatePicker(
        on_change=lambda _: on_date_change(date_picker.value),
        first_date=datetime.datetime.combine(datetime.date(2022, 1, 1), datetime.time()),
    )
    page.overlay.append(date_picker)
    return ft.Container(
        width=35,
        height=35,
        alignment=ft.alignment.center,
        content=ft.Icon(
            name=ft.icons.CALENDAR_MONTH_SHARP,
            size=15,
            opacity=0.65
        ),
        on_click=lambda _: page.open(date_picker)
    )
