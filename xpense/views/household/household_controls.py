import calendar
import datetime
from typing import List, Optional, Callable

import flet as ft
from flet_core import PopupMenuPosition, ControlEvent

from xpense.database.repository_container import RepositoryContainer
from xpense.types import DataAggregation, Transaction, Currency, TransactionType
from xpense.utilities.common import round_to_two_decimals, human_readable_datetime
from xpense.views.household.transaction_add_view import get_transaction_add_view, TransactionAddPipe, CURRENCY_TO_ICONS
from xpense.views.household.transaction_category_button import DEFAULT_EXPENSE_CATEGORIES_WITH_ICONS


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
            content=ft.Image(src="assets/simple_wallet.png", color=ft.colors.WHITE),
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
        self._data_aggregation_text = ft.Text(
            ref=self._data_aggregation,
            text_align=ft.TextAlign.CENTER,
            size=13,
            weight=ft.FontWeight.BOLD
        )
        self._data_aggregation.current.value = DataAggregation.MONTHLY.value.upper()

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
            self._data_aggregation.current.value = DataAggregation.get_aggregation_type(text).value.upper()
            self._data_aggregation_text.value = DataAggregation.get_aggregation_type(text).value.upper()
            self._data_aggregation_text.update()

        return ft.PopupMenuButton(
            icon=ft.icons.ARROW_DROP_DOWN,
            items=[
                ft.PopupMenuItem(text=DataAggregation.MONTHLY.value.upper(), on_click=change_pop_menu),
                ft.PopupMenuItem(text=DataAggregation.YEARLY.value.upper(), on_click=change_pop_menu),
                ft.PopupMenuItem(text=DataAggregation.WEEKLY.value.upper(), on_click=change_pop_menu),
            ],
            menu_position=PopupMenuPosition.UNDER,
            enable_feedback=True
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


class TransactionTypeTabsSection:
    def __init__(self, on_tab_change_func: Callable[[ControlEvent], None]):
        self._on_tab_change_func = on_tab_change_func

    def _get_tabs(self) -> ft.Container:
        return ft.Container(
            # bgcolor=ft.colors.YELLOW_500,
            content=ft.Tabs(
                selected_index=0,
                animation_duration=150,
                expand=0,
                tabs=[
                    ft.Tab(text=text.value.capitalize())
                    for text in TransactionType
                ],
                top=True,
                tab_alignment=ft.TabAlignment.FILL,
                padding=0,
                on_change=self._on_tab_change_func
            )
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.top_left,
            height=70,
            bgcolor=ft.colors.TRANSPARENT,
            content=self._get_tabs()
        )


class FloatingButtonSection:
    def __init__(self, page: ft.Page, repository_container: RepositoryContainer, current_date: datetime.date):
        self._page = page
        self._current_date = current_date
        self._transaction = Transaction(date=self._current_date)
        self._transaction_add_pipe = TransactionAddPipe(transaction=self._transaction)
        self._view = get_transaction_add_view(
            self._page,
            back_button_callable=lambda _: self._click_go_back_button(),
            save_transaction_button_callable=lambda _: self._click_save_button(),
            transaction_add_pipe=self._transaction_add_pipe,
        )
        self._rc = repository_container

    def _get_floating_button(self) -> ft.FloatingActionButton:
        return ft.FloatingActionButton(
            content=ft.Icon(ft.icons.ADD),
            bgcolor=ft.colors.AMBER_300,
            shape=ft.RoundedRectangleBorder(radius=20),
            scale=0.9,
            hover_elevation=10,
            on_click=lambda _: self._click_floating_button(),
        )

    def _click_save_button(self):
        print(f"DEBUG: saving transaction: {self._transaction}")

        if not self._transaction.amount:
            self._transaction_add_pipe.transaction_section.amount_text_field.error_text = "Required"
            self._transaction_add_pipe.transaction_section.amount_container.bgcolor = ft.colors.YELLOW_100
            self._transaction_add_pipe.transaction_section.main_container.update()
            return

        if self._transaction.amount and self._transaction_add_pipe.transaction_section.amount_text_field.error_text:
            self._transaction_add_pipe.transaction_section.amount_text_field.error_text = ""
            self._transaction_add_pipe.transaction_section.amount_container.bgcolor = ft.colors.WHITE
            self._transaction_add_pipe.transaction_section.main_container.update()

        self._rc.transactions.add(self._transaction)
        self._click_go_back_button()

    def _click_go_back_button(self):
        self._page.views.pop()
        self._page.update()

    def _click_floating_button(self):
        self._reset_transaction()
        self._page.views.append(self._view)
        self._page.update()

    def _reset_transaction(self):
        self._transaction = Transaction(date=self._current_date, currency=Currency.EURO)
        self._transaction_add_pipe = TransactionAddPipe(transaction=self._transaction)
        self._view = get_transaction_add_view(
            self._page,
            back_button_callable=lambda _: self._click_go_back_button(),
            save_transaction_button_callable=lambda _: self._click_save_button(),
            transaction_add_pipe=self._transaction_add_pipe,
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.bottom_right,
            bgcolor=ft.colors.TRANSPARENT,
            content=self._get_floating_button(),
            padding=ft.padding.only(right=15, bottom=15),
            height=80,
            width=80,
        )


class TransactionListViewSection:
    def __init__(self, page: ft.Page, repository_container: RepositoryContainer):
        self._page = page
        self._rc = repository_container

        self._list_view: Optional[ft.ListView] = None

    def on_tab_change(self, event: ControlEvent):
        selected_tab = event.control.tabs[event.control.selected_index]
        selected_transaction_type = TransactionType.get_transaction_type(selected_tab.text)
        self._list_view.controls = []
        self._populate_list_view(self._list_view, selected_transaction_type)
        self._list_view.update()

    def get(self):
        if not self._list_view:
            self._list_view = ft.ListView(
                spacing=1, padding=0, auto_scroll=False,
                expand=True,
                on_scroll=(lambda _: self._page.update())
            )
        self._populate_list_view(self._list_view, TransactionType.EXPENSE)  # The default is to populate expense type.
        return self._list_view

    def _populate_list_view(self, list_view: ft.ListView, populate_transaction_type: TransactionType):
        transactions: List[Transaction] = self._rc.transactions.get_all()

        for transaction in transactions:
            if transaction.type != populate_transaction_type:
                continue

            list_view.controls.append(
                ft.Container(
                    alignment=ft.alignment.center_left,
                    bgcolor=ft.colors.GREY_100,
                    padding=ft.padding.only(left=10, right=10),
                    height=60,
                    content=ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(DEFAULT_EXPENSE_CATEGORIES_WITH_ICONS.get(transaction.category), size=40),
                                    ft.Column(
                                        controls=[ft.Text(value=transaction.category.title()),
                                                  ft.Text(value=human_readable_datetime(transaction.date),
                                                          size=10)],
                                        spacing=0, alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(CURRENCY_TO_ICONS.get(transaction.currency), size=12,
                                            color=ft.colors.RED_500),
                                    ft.Text(value=round_to_two_decimals(transaction.amount), color=ft.colors.RED_500,
                                            size=13),
                                ],
                                spacing=2, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.alignment.center
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )


def get_main_container(
        page: ft.Page,
        repository_container: RepositoryContainer,
        setup_currency_type: Currency,
        data_aggregation: ft.Ref[ft.Text],
        current_date: datetime.datetime,
) -> ft.Container:
    transaction_list_view_section = TransactionListViewSection(page=page, repository_container=repository_container)
    transaction_type_tabs_section = TransactionTypeTabsSection(
        on_tab_change_func=transaction_list_view_section.on_tab_change
    )

    return ft.Container(
        alignment=ft.alignment.top_center,
        expand=True,
        bgcolor=ft.colors.WHITE70,
        margin=-10,
        content=ft.Column(
            controls=[
                OverviewSection().get(),
                DateSection(current_date, data_aggregation).get(),
                transaction_type_tabs_section.get(),
                ft.Stack(
                    controls=[
                        transaction_list_view_section.get(),
                        FloatingButtonSection(page, repository_container, current_date).get(),
                    ],
                    expand=True,
                    alignment=ft.alignment.bottom_right,
                )
            ],
            # expand=True,
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        )
    )


def get_household_controls(
        page: ft.Page,
        repository_container: RepositoryContainer,
        setup_currency_type: Currency,
        data_aggregation: ft.Ref[ft.Text],
        current_date: datetime.datetime,
) -> List[ft.Control]:
    return [get_main_container(page, repository_container, setup_currency_type, data_aggregation, current_date)]
