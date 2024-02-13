from typing import List

import flet as ft

from bugbro.views.household.action_button import get_action_button


def get_household_container() -> ft.Container:
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Balance Overview", size=20),
            ], expand=True),
            ft.Row([
                ft.Text("Date Section"),
            ], expand=True),
            ft.Row([
                ft.TextButton("Income", on_click=lambda e: print("Income")),
                ft.TextButton("Expenses", on_click=lambda e: print("Expenses")),
            ]),
            get_action_button()
        ]),
        bgcolor=ft.colors.BLUE_100,  # Background color of the container
        expand=True,
        margin=ft.margin.all(0),
    )


def get_household_controls() -> List[ft.Control]:
    return [get_household_container()]
