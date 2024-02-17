import calendar
import datetime
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


def get_main_column() -> ft.Column:
    return ft.Column(
        expand=True,
        controls=[
            ft.Row(
                height=100,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height=200,
                        # width=100,
                        expand=True,
                        bgcolor=ft.colors.GREEN_ACCENT
                    )
                ],
            )
        ],
        alignment=ft.MainAxisAlignment.START,
    )


class OverviewSection:
    def _get_wallet_image_container(self) -> ft.Container:
        return ft.Container(
            height=50,
            width=75,
            content=ft.Image(src="simple_wallet.png", color=ft.colors.WHITE),
            padding=ft.padding.only(left=15, top=10),
            alignment=ft.alignment.top_left
        )

    def _get_first_column_balance_label_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Text("Balance This Month", color=ft.colors.WHITE, size=13),
            padding=ft.padding.only(left=15, top=2),
            alignment=ft.alignment.top_left
        )

    def _get_first_column_balance_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Text("€ 10.00", color=ft.colors.WHITE, size=15, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(left=15),
            alignment=ft.alignment.top_left
        )

    def _get_first_column(self) -> ft.Column:
        return ft.Column(
            width=170,
            controls=[
                self._get_wallet_image_container(),
                self._get_first_column_balance_label_container(),
                self._get_first_column_balance_container(),
            ],
        )

    def _get_second_column(self) -> ft.Column:
        return ft.Column(
            width=125,
            controls=[
                ft.Container(
                    padding=ft.padding.only(top=20),
                    content=ft.Column(
                        alignment=ft.alignment.top_left,
                        controls=[
                            ft.Text(
                                value="Income",
                                color=ft.colors.WHITE,
                                size=13,
                            ),
                            ft.Text(
                                value="Expense",
                                color=ft.colors.WHITE,
                                size=13,
                            ),
                            ft.Text(
                                value="Allocated",
                                color=ft.colors.WHITE,
                                size=13,
                            ),
                        ]
                    )
                )

            ]
        )

    def _get_third_column(self) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.top_right,
                    padding=ft.padding.only(top=20),
                    content=ft.Column(
                        alignment=ft.alignment.top_right,
                        controls=[
                            ft.Text(
                                value="€ 10.00",
                                color=ft.colors.WHITE,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value="€ 10.00",
                                color=ft.colors.WHITE,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                value="€ 10.00",
                                color=ft.colors.WHITE,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ]
                    )
                )

            ]
        )

    def _get_main_row(self) -> ft.Row:
        return ft.Row(
            expand=True,
            controls=[
                self._get_first_column(),
                self._get_second_column(),
                self._get_third_column(),
            ],
            spacing=0,
        )

    def _get_main_container(self) -> ft.Container:
        return ft.Container(
            height=120,
            bgcolor=ft.colors.SURFACE_VARIANT,
            expand=True,
            theme=ft.Theme(color_scheme_seed=ft.colors.BLUE_50),
            theme_mode=ft.ThemeMode.LIGHT,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[ft.colors.BLUE_700, ft.colors.RED_400]
            ),
            content=self._get_main_row()
        )

    def get(self) -> ft.Row:
        return ft.Row(
            alignment=ft.alignment.top_center,
            height=120,
            controls=[
                self._get_main_container()
            ],
            spacing=0,
        )


class DateSection:
    def __init__(self, current_date: datetime.date):
        self._date = current_date

    def _get_month_name_container(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(value=calendar.month_name[self._date.month], text_align=ft.TextAlign.CENTER),
            alignment=ft.alignment.center
        )

    def _get_pop_menu_button_container(self) -> ft.Column:
        # return ft.Container(
        #     expand=True,
        #     content=ft.Column(
        #         controls=[ft.PopupMenuButton(
        #             icon=ft.icons.ARROW_DROP_DOWN,
        #         )],
        #         alignment=ft.MainAxisAlignment.START,
        #         horizontal_alignment=ft.alignment.center,
        #     )
        # )
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.alignment.center,
                    ),
                    bgcolor=ft.colors.AMBER_100,
                    height=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.alignment.center,
        )

    def _get_main_container(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.top_left,
            height=70,
            expand=True,
            border=ft.border.only(
                top=ft.BorderSide(0.9, ft.colors.BLACK),
                bottom=ft.BorderSide(0.9, ft.colors.BLACK)
            ),
            bgcolor=ft.colors.BLUE_100,
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        height=25,
                        controls=[
                            self._get_pop_menu_button_container()
                        ],
                    ),
                    ft.Row(
                        spacing=0,
                        alignment=ft.alignment.center_left,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[self._get_month_name_container()]
                    )
                ]
            ),
        )

    def get(self) -> ft.Row:
        return ft.Row(
            height=70,
            alignment=ft.alignment.top_center,
            controls=[
                self._get_main_container()
            ],
            spacing=0,
        )


def get_main_container(current_date: datetime.date) -> ft.Container:
    return ft.Container(
        alignment=ft.alignment.top_center,
        expand=True,
        bgcolor=ft.colors.WHITE70,
        margin=-10,
        content=ft.Column(
            controls=[
                OverviewSection().get(),
                DateSection(current_date).get()
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        )
    )


def get_household_controls(current_date: datetime.date) -> List[ft.Control]:
    return [get_main_container(current_date)]
