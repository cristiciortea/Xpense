import calendar
import datetime
from typing import List, Optional, Callable, Tuple

import flet as ft
from flet_core import PopupMenuPosition, ControlEvent

from xpense.database.repository_container import RepositoryContainer
from xpense.types import Transaction, Currency, TransactionType, TransactionOperations, \
    DataAggregation
from xpense.utilities.common import round_to_two_decimals, human_readable_datetime
from xpense.views.household.balance_calculator import BalanceCalculator
from xpense.views.household.transaction_category_button import DEFAULT_EXPENSE_CATEGORIES_WITH_ICONS
from xpense.views.household.transaction_fetcher import TransactionFetcher
from xpense.views.household.transaction_view import get_transaction_view, TransactionPipe, CURRENCY_TO_ICONS


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
    def __init__(
            self, repository_container: RepositoryContainer, current_datetime: datetime.datetime,
            data_aggregation: DataAggregation
    ):
        self._calculator = BalanceCalculator(repository_container, current_datetime)
        self._data_aggregation = data_aggregation

        self._expenses_amount = None
        self._income_amount = None
        self._allocations_amount = None
        self._expenses_amount_ref = ft.Ref[ft.Text]()
        self._income_amount_ref = ft.Ref[ft.Text]()
        self._allocations_amount_ref = ft.Ref[ft.Text]()
        self._build_column_three_amount_texts()
        self._set_amounts()

        self._container_first_column_text_label_ref = ft.Ref[ft.Text]()
        self._first_column_total_balance_text_label_ref = ft.Ref[ft.Text]()

    def _build_column_three_amount_texts(self):
        self._income_amount = ft.Text(
            ref=self._income_amount_ref,
            color=ft.colors.WHITE,
            size=13,
            weight=ft.FontWeight.BOLD,
        )
        self._expenses_amount = ft.Text(
            ref=self._expenses_amount_ref,
            color=ft.colors.WHITE,
            size=13,
            weight=ft.FontWeight.BOLD,
        )
        self._allocations_amount = ft.Text(
            ref=self._allocations_amount_ref,
            color=ft.colors.WHITE,
            size=13,
            weight=ft.FontWeight.BOLD,
        )

    def _set_amounts(self, data_aggregation: Optional[DataAggregation] = None):
        if not data_aggregation:
            data_aggregation = self._data_aggregation
        self._expenses_amount_ref.current.value = f"€ {self._calculator.get_total_expenses(data_aggregation)}"
        self._income_amount_ref.current.value = f"€ {self._calculator.get_total_income()}"
        self._allocations_amount_ref.current.value = f"€ {self._calculator.get_total_allocations()}"

    def _determine_first_column_container_label_text(self, data_aggregation: Optional[DataAggregation] = None):
        if not data_aggregation:
            data_aggregation = self._data_aggregation

        if data_aggregation == DataAggregation.MONTHLY:
            aggregation_label = "month"
        elif data_aggregation == DataAggregation.WEEKLY:
            aggregation_label = "week"
        else:
            aggregation_label = "year"
        return f"Balance This {aggregation_label.title()}"

    def _determine_first_column_total_balance_label_text(self, data_aggregation: Optional[DataAggregation] = None):
        total_balance = self._calculator.get_total_balance(data_aggregation)
        return f"€ {total_balance}"

    def on_data_aggregation_change(self, event: ControlEvent):
        new_data_aggregation = DataAggregation.get_aggregation_type(event.control.text)
        self._set_amounts(new_data_aggregation)
        self._container_first_column_text_label_ref.current.value = self._determine_first_column_container_label_text(
            new_data_aggregation
        )
        self._first_column_total_balance_text_label_ref.current.value = self._determine_first_column_total_balance_label_text(
            new_data_aggregation
        )

    def _get_wallet_image_container(self) -> ft.Container:
        return ft.Container(
            height=46,
            width=75,
            content=ft.Image(
                src="assets/simple_wallet.png", color=ft.colors.WHITE,
            ),
        )

    def _get_first_column_balance_label_container(self) -> ft.Container:

        return ft.Container(
            content=ft.Text(
                self._determine_first_column_container_label_text(),
                color=ft.colors.WHITE, size=13, width=120,
                ref=self._container_first_column_text_label_ref,
            ),
            padding=ft.padding.only(left=15, top=2),
            alignment=ft.alignment.top_left,
        )

    def _get_first_column_balance_container(self) -> ft.Container:
        label_text = self._determine_first_column_total_balance_label_text()
        return ft.Container(
            content=ft.Text(
                label_text, color=ft.colors.WHITE, size=15, weight=ft.FontWeight.BOLD.value,
                tooltip="Shows overall financial status after accounting for both expenses and allocations.",
                ref=self._first_column_total_balance_text_label_ref,
            ),
            padding=ft.padding.only(left=15),
            alignment=ft.alignment.top_left
        )

    def _get_first_column(self) -> ft.Container:
        return ft.Container(
            # bgcolor=ft.colors.TEAL_ACCENT,
            width=130,
            content=ft.Column(
                spacing=0,
                controls=[
                    self._get_wallet_image_container(),
                    self._get_first_column_balance_label_container(),
                    self._get_first_column_balance_container(),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            margin=ft.margin.only(left=2),
        )

    def _get_second_column_labels(self) -> ft.Container:
        return ft.Container(
            # bgcolor=ft.colors.YELLOW,
            alignment=ft.alignment.center_right,
            padding=ft.padding.only(right=20),
            width=130,
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
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
                        value="Allocation",
                        color=ft.colors.WHITE,
                        size=13,
                    ),
                ]
            )
        )

    def _get_third_column_amount(self) -> ft.Container:
        return ft.Container(
            # bgcolor=ft.colors.BLUE,
            alignment=ft.alignment.top_center,
            width=130,
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                controls=[
                    self._income_amount,
                    self._expenses_amount,
                    self._allocations_amount
                ]
            )
        )

    def _get_main_row(self) -> ft.Row:
        return ft.Row(
            expand=True,
            controls=[
                self._get_first_column(),
                self._get_second_column_labels(),
                self._get_third_column_amount(),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def get(self) -> ft.Container:
        return ft.Container(
            height=150,
            padding=0,
            margin=0,
            bgcolor=ft.colors.SURFACE_VARIANT,
            theme=ft.Theme(color_scheme_seed=ft.colors.BLUE_50),
            theme_mode=ft.ThemeMode.LIGHT,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[ft.colors.BLUE_700, ft.colors.RED_400]
            ),
            content=self._get_main_row(),
        )


class DateSection:
    def __init__(
            self,
            page: ft.Page,
            current_date: datetime.datetime,
            data_aggregation: DataAggregation,
            data_aggregation_change_callbacks: Optional[Tuple[Callable, ...]] = None
    ):
        self._page = page
        self._current_date = current_date

        self._data_aggregation = data_aggregation
        self._data_aggregation_text_ref = ft.Ref[ft.Text]()
        self._data_aggregation_text = ft.Text(
            ref=self._data_aggregation_text_ref,
            text_align=ft.TextAlign.CENTER,
            size=13,
            weight=ft.FontWeight.BOLD
        )
        self._data_aggregation_text_ref.current.value = self._data_aggregation.MONTHLY.value.upper()
        self._data_aggregation_change_callbacks = data_aggregation_change_callbacks

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

    def _change_data_aggregation(self, event: ft.ControlEvent):
        text = event.control.text
        self._data_aggregation = DataAggregation.get_aggregation_type(text).value.upper()
        self._data_aggregation_text.value = DataAggregation.get_aggregation_type(text).value.upper()

        for callback in self._data_aggregation_change_callbacks:
            callback(event)

        self._page.update()

    def _get_pop_menu_data_aggregation_button(self) -> ft.PopupMenuButton:
        return ft.PopupMenuButton(
            icon=ft.icons.ARROW_DROP_DOWN,
            items=[
                ft.PopupMenuItem(text=DataAggregation.MONTHLY.value.upper(),
                                 on_click=lambda event: self._change_data_aggregation(event)),
                ft.PopupMenuItem(text=DataAggregation.YEARLY.value.upper(),
                                 on_click=lambda event: self._change_data_aggregation(event)),
                ft.PopupMenuItem(text=DataAggregation.WEEKLY.value.upper(),
                                 on_click=lambda event: self._change_data_aggregation(event)),
            ],
            menu_position=PopupMenuPosition.UNDER,
            enable_feedback=True
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.top_left,
            height=70,
            bgcolor=ft.colors.RED_100,
            # gradient=ft.LinearGradient(
            #     begin=ft.alignment.center_left,
            #     end=ft.alignment.center_right,
            #     colors=[ft.colors.BLUE_GREY_50, ft.colors.RED_100, ft.colors.BLUE_GREY_50]
            # ),
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Row(
                        spacing=0,
                        controls=[
                            self._data_aggregation_text,
                            self._get_pop_menu_data_aggregation_button()
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

    def get(self) -> ft.Tabs:
        return ft.Tabs(
            selected_index=0,
            animation_duration=50,
            tabs=[
                ft.Tab(text=text.value.capitalize())
                for text in TransactionType
            ],
            top=True,
            tab_alignment=ft.TabAlignment.FILL,
            padding=0,
            divider_color=ft.colors.BLACK12,
            on_change=self._on_tab_change_func,
            indicator_tab_size=True,
            indicator_thickness=True,
        )


class FloatingButtonSection:
    def __init__(
            self, page: ft.Page, repository_container: RepositoryContainer, current_date: datetime.datetime,
            setup_currency_type: Currency,
    ):
        self._page = page
        self._current_date = current_date
        self._setup_currency_type = setup_currency_type

        self._transaction = self._get_default_transaction()
        self._transaction_pipe = TransactionPipe(transaction=self._transaction)
        self._view = get_transaction_view(
            page=self._page,
            transaction_pipe=self._transaction_pipe,
            back_button_callable=lambda _: self._click_go_back_button(),
            save_transaction_button_callable=lambda _: self._click_save_button(),
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
        if not self._transaction.amount:
            self._transaction_pipe.transaction_section.amount_text_field.error_text = "Required"
            self._transaction_pipe.transaction_section.amount_container.bgcolor = ft.colors.YELLOW_100
            self._transaction_pipe.transaction_section.main_container.update()
            return

        if self._transaction.amount and self._transaction_pipe.transaction_section.amount_text_field.error_text:
            self._transaction_pipe.transaction_section.amount_text_field.error_text = ""
            self._transaction_pipe.transaction_section.amount_container.bgcolor = ft.colors.WHITE
            self._transaction_pipe.transaction_section.main_container.update()

        self._rc.transactions.add(self._transaction)
        self._click_go_back_button()

    def _click_go_back_button(self):
        self._page.views.pop()
        self._page.update()

    def _click_floating_button(self):
        self._reset_transaction()
        self._page.views.append(self._view)
        self._page.update()

    def _get_default_transaction(self):
        return Transaction(
            type=TransactionType.EXPENSE, date=self._current_date, currency=self._setup_currency_type,
            category="other", aggregation=DataAggregation.MONTHLY,
        )

    def _reset_transaction(self):
        self._transaction = self._get_default_transaction()
        self._transaction_pipe = TransactionPipe(transaction=self._transaction)
        self._view = get_transaction_view(
            page=self._page,
            transaction_pipe=self._transaction_pipe,
            back_button_callable=lambda _: self._click_go_back_button(),
            save_transaction_button_callable=lambda _: self._click_save_button(),
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


class TransactionEditContainer:
    def __init__(
            self,
            page: ft.Page,
            repository_container: RepositoryContainer
    ):
        self._page = page
        self._rc = repository_container

    def _click_go_back_button(self):
        self._page.views.pop()
        self._page.update()

    def _click_save_button(self, transaction_pipe: TransactionPipe):
        transaction = transaction_pipe.transaction

        if not transaction.amount:
            transaction_pipe.transaction_section.amount_text_field.error_text = "Required"
            transaction_pipe.transaction_section.amount_container.bgcolor = ft.colors.YELLOW_100
            transaction_pipe.transaction_section.main_container.update()
            return

        if transaction.amount and transaction_pipe.transaction_section.amount_text_field.error_text:
            transaction_pipe.transaction_section.amount_text_field.error_text = ""
            transaction_pipe.transaction_section.amount_container.bgcolor = ft.colors.WHITE
            transaction_pipe.transaction_section.main_container.update()

        self._rc.transactions.update(transaction)
        self._click_go_back_button()

    def _click_delete_transaction_button(self, transaction_pipe: TransactionPipe):
        transaction = transaction_pipe.transaction
        self._rc.transactions.delete(Transaction, transaction.id)
        self._click_go_back_button()

    def on_click_edit_container(self, event: ControlEvent):
        transaction_id = event.control.data
        transaction = self._rc.transactions.get_by_id(Transaction, transaction_id)
        transaction_pipe = TransactionPipe(transaction=transaction)

        view = get_transaction_view(
            page=self._page,
            transaction_pipe=transaction_pipe,
            back_button_callable=lambda _: self._click_go_back_button(),
            save_transaction_button_callable=lambda _: self._click_save_button(transaction_pipe),
            delete_transaction_button_callable=lambda _: self._click_delete_transaction_button(transaction_pipe),
            transaction_operation=TransactionOperations.EDIT,
        )
        self._page.views.append(view)
        self._page.update()


class TransactionListViewSection:
    def __init__(
            self, page: ft.Page, repository_container: RepositoryContainer,
            transaction_edit_container: TransactionEditContainer,
            data_aggregation: DataAggregation,
            current_datetime: datetime.datetime,
    ):
        self._page = page
        self._rc = repository_container
        self._transaction_edit_container = transaction_edit_container
        self._transaction_fetcher = TransactionFetcher(repository_container, current_datetime)

        self._data_aggregation = data_aggregation

        self._list_view: Optional[ft.ListView] = None

    def on_data_aggregation_change(self, event: ControlEvent):
        self._list_view.controls = []
        self._populate_list_view(
            self._list_view,
            populate_transaction_type=TransactionType.EXPENSE,
            data_aggregation=DataAggregation.get_aggregation_type(event.control.text)
        )
        self._list_view.update()

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
        self._populate_list_view(
            self._list_view,
            populate_transaction_type=TransactionType.EXPENSE,
            data_aggregation=self._data_aggregation
        )
        return self._list_view

    def _populate_list_view(
            self, list_view: ft.ListView, populate_transaction_type: TransactionType,
            data_aggregation: Optional[DataAggregation] = DataAggregation.MONTHLY
    ):
        transactions: List[Transaction] = self._transaction_fetcher.get_by_type(
            populate_transaction_type, data_aggregation
        )

        for transaction in transactions:
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
                    data=transaction.id,
                    on_click=self._transaction_edit_container.on_click_edit_container,
                )
            )


def get_main_container(
        page: ft.Page,
        repository_container: RepositoryContainer,
        setup_currency_type: Currency,
        data_aggregation: DataAggregation,
        current_date: datetime.datetime,
) -> ft.Container:
    transaction_edit_container = TransactionEditContainer(page=page, repository_container=repository_container)
    transaction_list_view_section = TransactionListViewSection(
        page=page, repository_container=repository_container, transaction_edit_container=transaction_edit_container,
        data_aggregation=data_aggregation, current_datetime=current_date
    )
    transaction_type_tabs_section = TransactionTypeTabsSection(
        on_tab_change_func=transaction_list_view_section.on_tab_change
    )
    overview_section = OverviewSection(repository_container=repository_container, current_datetime=current_date,
                                       data_aggregation=data_aggregation)
    date_section = DateSection(
        page, current_date, data_aggregation,
        data_aggregation_change_callbacks=(
            transaction_list_view_section.on_data_aggregation_change,
            overview_section.on_data_aggregation_change)
    )

    return ft.Container(
        alignment=ft.alignment.top_center,
        expand=True,
        padding=0,
        margin=0,
        bgcolor=ft.colors.WHITE70,
        content=ft.Column(
            controls=[
                overview_section.get(),
                date_section.get(),
                transaction_type_tabs_section.get(),
                ft.Stack(
                    controls=[
                        transaction_list_view_section.get(),
                        FloatingButtonSection(
                            page, repository_container, current_date, setup_currency_type
                        ).get(),
                    ],
                    expand=True,
                    alignment=ft.alignment.bottom_right,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        )
    )


def get_household_controls(
        page: ft.Page,
        repository_container: RepositoryContainer,
        setup_currency_type: Currency,
        data_aggregation: DataAggregation,
        current_date: datetime.datetime,
) -> List[ft.Control]:
    return [get_main_container(page, repository_container, setup_currency_type, data_aggregation, current_date)]
