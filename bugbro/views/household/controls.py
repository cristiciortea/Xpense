import calendar
import datetime
from typing import List, Optional

import flet as ft

from bugbro.types import DataAggregation, Routes
from bugbro.views.household.action_button import get_action_button
from bugbro.views.household.transactions_view import get_transactions_view


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

    def get(self) -> ft.Container:
        return ft.Container(
            height=120,
            bgcolor=ft.colors.SURFACE_VARIANT,
            theme=ft.Theme(color_scheme_seed=ft.colors.BLUE_50),
            theme_mode=ft.ThemeMode.LIGHT,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[ft.colors.BLUE_700, ft.colors.RED_400]
            ),
            content=self._get_main_row()
        )


class DateSection:
    def __init__(
            self,
            current_date: datetime.date,
            data_aggregation: ft.Ref[ft.Text]
    ):
        self._current_date = current_date

        self._data_aggregation = data_aggregation
        self._data_aggregation_text = ft.Text(ref=self._data_aggregation,
                                              text_align=ft.TextAlign.CENTER,
                                              size=13,
                                              weight=ft.FontWeight.BOLD)
        self._data_aggregation.current.value = DataAggregation.MONTHLY.value

    def _get_data_aggregation_label_container(self) -> ft.Container:
        month_name = calendar.month_name[self._current_date.month].upper()
        year = self._current_date.year
        return ft.Container(
            content=ft.Text(value=f"{month_name} {year}",
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD,
                            size=13),
            alignment=ft.alignment.center
        )

    def _get_pop_menu_button(self) -> ft.PopupMenuButton:
        def change_pop_menu(event: ft.ControlEvent):
            text = event.control.text
            self._data_aggregation.current.value = DataAggregation(text).value
            self._data_aggregation_text.value = DataAggregation(text).value
            self._data_aggregation_text.update()

        return ft.PopupMenuButton(
            icon=ft.icons.ARROW_DROP_DOWN,
            items=[
                ft.PopupMenuItem(text=DataAggregation.MONTHLY.value, on_click=change_pop_menu),
                ft.PopupMenuItem(text=DataAggregation.YEARLY.value, on_click=change_pop_menu),
                ft.PopupMenuItem(text=DataAggregation.WEEKLY.value, on_click=change_pop_menu),
            ],
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.top_left,
            height=70,
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
                        controls=[
                            self._data_aggregation_text,
                            self._get_pop_menu_button()
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Row(
                            spacing=0,
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[self._get_data_aggregation_label_container()],
                        ),
                        padding=ft.padding.only(left=20)
                    )
                ]
            ),
        )


class TabsSection:
    def _get_tabs(self) -> ft.Tabs:
        return ft.Tabs(
            selected_index=0,
            animation_duration=150,
            expand=0,
            tabs=[
                ft.Tab(
                    text="Income",
                ),
                ft.Tab(
                    text="Expense",
                ),
                ft.Tab(
                    text="Allocations",
                ),
            ],
            top=True,
            tab_alignment=ft.TabAlignment.FILL
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.top_left,
            height=70,
            bgcolor=ft.colors.TRANSPARENT,
            content=self._get_tabs()
        )


class FloatingButtonSection:
    def __init__(self, page: ft.Page, current_date: datetime.date):
        self._page = page
        self._current_date = current_date
        self._view = get_transactions_view(self._page, back_button_callable=lambda _: self._click_go_back_button(),
                                           current_date=current_date)

    def _click_go_back_button(self):
        self._page.views.pop()
        self._page.update()

    def _click_floating_button(self):
        self._page.views.append(self._view)
        self._page.update()

    def _get_button(self) -> ft.FloatingActionButton:
        return ft.FloatingActionButton(
            content=ft.Icon(ft.icons.ADD),
            bgcolor=ft.colors.AMBER_300,
            shape=ft.RoundedRectangleBorder(radius=20),
            scale=0.9,
            on_click=lambda _: self._click_floating_button()
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.bottom_right,
            bgcolor=ft.colors.TRANSPARENT,
            content=self._get_button(),
            expand=True,
            padding=ft.padding.only(right=15, bottom=15)
        )


def get_main_container(current_date: datetime.date, data_aggregation: ft.Ref[ft.Text],
                       page: ft.Page) -> ft.Container:
    return ft.Container(
        alignment=ft.alignment.top_center,
        expand=True,
        bgcolor=ft.colors.WHITE70,
        margin=-10,
        content=ft.Column(
            controls=[
                OverviewSection().get(),
                DateSection(current_date, data_aggregation).get(),
                TabsSection().get(),
                FloatingButtonSection(page, current_date).get(),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        )
    )


def get_household_controls(
        current_date: datetime.date, data_aggregation: ft.Ref[ft.Text], page: ft.Page
) -> List[ft.Control]:
    return [get_main_container(current_date, data_aggregation, page)]
