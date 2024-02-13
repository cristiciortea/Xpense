import flet as ft
from flet_core import MainAxisAlignment


def get_action_button():
    return ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.ADD)], alignment=MainAxisAlignment.CENTER, spacing=2
        ),
        bgcolor=ft.colors.AMBER_300,
        shape=ft.RoundedRectangleBorder(radius=15),
        width=100,
        mini=True,
        bottom=True,
    )
