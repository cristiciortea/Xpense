import dataclasses
import datetime
from typing import Callable, Optional

import flet as ft

from xpense.types import TransactionType, Transaction, Currency, TransactionOperations
from xpense.utilities.calendar import convert_datetime_to_string
from xpense.utilities.common import round_to_two_decimals
from xpense.utilities.household import keep_first_dot
from xpense.views.household.transaction_category_button import TransactionCategoryButton

CURRENCY_TO_ICONS = {
    Currency.EURO: ft.icons.EURO,
    Currency.DOLLAR: ft.icons.ATTACH_MONEY,
    Currency.RON: ft.icons.MONEY
}


class SegmentButton:
    def __init__(self, transaction: Transaction):
        self._transaction = transaction
        self._transaction_type = self._transaction.type

    def _on_change(self, event: ft.ControlEvent):
        self._transaction.type = TransactionType.get_transaction_type(next(iter(event.control.selected)))

    def _get_segment_button(self) -> ft.SegmentedButton:
        return ft.SegmentedButton(
            on_change=lambda event: self._on_change(event),
            width=380,
            selected={self._transaction_type.value},
            expand_loose=False,
            expand=True,
            segments=[
                ft.Segment(
                    value=TransactionType.EXPENSE.value,
                    label=ft.Text(TransactionType.EXPENSE.value.capitalize()),
                ),
                ft.Segment(
                    value=TransactionType.INCOME.value,
                    label=ft.Text(TransactionType.INCOME.value.capitalize()),
                ),
                ft.Segment(
                    value=TransactionType.ALLOCATION.value,
                    label=ft.Text(TransactionType.ALLOCATION.value.capitalize()),
                ),
            ],
            scale=0.9,
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.center,
            content=self._get_segment_button(),
            padding=ft.padding.only(top=25, bottom=15)
        )


class TransactionInputSection:
    def __init__(self, page: ft.Page, transaction_pipe: "TransactionPipe"):
        self._page = page
        self._transaction_pipe = transaction_pipe
        self._transaction_pipe.transaction_section = self
        self._transaction = self._transaction_pipe.transaction

        self._current_date = self._transaction.date
        self.amount_text_field: Optional[ft.TextField] = None
        self.main_container: Optional[ft.Container] = None
        self.amount_container: Optional[ft.Container] = None

        self._date_picker = ft.DatePicker(
            on_change=lambda _: self._on_date_change(self._date_picker.value),
            first_date=datetime.datetime.combine(self._current_date - datetime.timedelta(days=365), datetime.time()),
            current_date=self._transaction.date,
        )
        self._page.overlay.append(self._date_picker)

        self._category_label_ref = ft.Ref[ft.Text]()
        self._category_button = TransactionCategoryButton(self._page, self._category_label_ref, self._transaction)

        # self._prepopulate_with_data_if_available_on_transaction()

    def _prepopulate_with_data_if_available_on_transaction(self):
        self.amount_text_field.value = self._transaction.amount
        self.amount_text_field.update()

    def _on_date_change(self, target_date: datetime.datetime):
        transaction_date = datetime.datetime.combine(target_date, datetime.datetime.now().time())
        self._transaction.date = transaction_date

    def _on_text_field_change(self, event: ft.ControlEvent):
        amount = event.control.value

        # Allow only digits and a single dot.
        amount = ''.join(c for c in amount if c.isdigit() or c == '.')
        amount = keep_first_dot(amount)

        # Limit to 7 digits before the dot.
        amount = amount[:7]

        # Update the text field.
        self._transaction.amount = amount
        self.amount_text_field.value = amount
        self.amount_text_field.update()

    def _on_currency_change(self, event: ft.ControlEvent):
        selected_text = event.control.text
        selected_currency = Currency.get_currency_type(selected_text)
        menu_button = event.control.parent
        self._transaction.currency = selected_currency
        menu_button.icon = CURRENCY_TO_ICONS.get(selected_currency)
        menu_button.update()

    def _build_input_amount_text_field(self) -> ft.TextField:
        if self.amount_text_field is None:
            self.amount_text_field = ft.TextField(
                # bgcolor=ft.colors.BLACK,
                value="" if not self._transaction.amount else round_to_two_decimals(self._transaction.amount),
                adaptive=True,
                on_change=lambda event: self._on_text_field_change(event),
                border=ft.InputBorder.NONE,
                width=55,
                height=49,
                multiline=False,
                max_lines=1,
                text_align=ft.TextAlign.END,
                text_vertical_align=ft.VerticalAlignment.START,
                keyboard_type=ft.KeyboardType.PHONE,
                text_size=13.8,
                hint_text="0.00",
                hint_style=ft.TextStyle(size=13.8, weight=ft.FontWeight.NORMAL)
                # fill_color=ft.colors.BLUE_600
            )
        return self.amount_text_field

    def get_date_container(self) -> ft.Container:
        return ft.Container(
            # bgcolor=ft.colors.BLUE,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Date", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(convert_datetime_to_string(self._current_date).split()[0]),
                        on_click=lambda _: self._date_picker.pick_date())
                ],
                spacing=0,
            )
        )

    def _get_currency_pop_menu(self):
        return ft.PopupMenuButton(
            icon=ft.icons.EURO,
            items=[
                ft.PopupMenuItem(text=Currency.RON.value, on_click=self._on_currency_change),
                ft.PopupMenuItem(text=Currency.EURO.value, on_click=self._on_currency_change),
                ft.PopupMenuItem(text=Currency.DOLLAR.value, on_click=self._on_currency_change),
            ],
            elevation=2,
            tooltip="Change currency",
            icon_size=14,
            width=14,
        )

    def get_amount_container(self) -> ft.Container:
        if not self.amount_container:
            self.amount_container = ft.Container(
                # bgcolor=ft.colors.BLUE,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Amount", weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[
                                self._get_currency_pop_menu(),
                                self._build_input_amount_text_field(),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        )

                    ],
                    spacing=0
                )
            )
        return self.amount_container

    def get_category_container(self) -> ft.Container:
        return ft.Container(
            # bgcolor=ft.colors.BLUE,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Category", weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            ft.Text(self._transaction.category.title(), ref=self._category_label_ref),
                            ft.IconButton(
                                icon=ft.icons.ARROW_DROP_DOWN,
                                on_click=lambda event: self._category_button.open_dialog(event)
                            )
                        ],
                        spacing=5,
                    )
                ],
                spacing=0,
            )
        )

    def get(self) -> ft.Container:
        if not self.main_container:
            self.main_container = ft.Container(
                content=ft.Column(controls=[
                    self.get_date_container(),
                    self.get_amount_container(),
                    self.get_category_container(),
                ],
                    spacing=1),
                # bgcolor=ft.colors.YELLOW,
                alignment=ft.alignment.center,
                margin=ft.margin.only(left=30, right=30),
            )
        return self.main_container


@dataclasses.dataclass
class TransactionPipe:
    transaction: Transaction
    transaction_section: Optional[TransactionInputSection] = None


class TransactionViewAppBar:
    def __init__(
            self,
            back_button_callable: Callable,
            delete_transaction_button_callable: Optional[Callable] = None
    ):
        self._back_button_callable = back_button_callable
        self._delete_transaction_button_callable = delete_transaction_button_callable

    def get(self) -> ft.BottomAppBar:
        app_bar_controls = [
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.WHITE,
                          on_click=self._back_button_callable),
            ft.Container(expand=True),
        ]

        if self._delete_transaction_button_callable:
            app_bar_controls.append(
                ft.IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.WHITE,
                              on_click=self._delete_transaction_button_callable),
            )

        return ft.BottomAppBar(
            bgcolor=ft.colors.BLUE,
            shape=ft.NotchShape.CIRCULAR,
            notch_margin=10,
            content=ft.Row(
                controls=app_bar_controls
            ),
        )


def get_transaction_view(
        page: ft.Page,
        transaction_pipe: TransactionPipe,
        back_button_callable: Callable,
        save_transaction_button_callable: Callable,
        delete_transaction_button_callable: Optional[Callable] = None,
        transaction_operation: Optional[TransactionOperations] = TransactionOperations.ADD,
) -> ft.View:
    transaction_view_appbar = TransactionViewAppBar(
        back_button_callable=back_button_callable,
        delete_transaction_button_callable=delete_transaction_button_callable,
    )
    if transaction_operation == TransactionOperations.ADD:
        transaction_view_headline = "Add transaction"
    else:
        transaction_view_headline = "Edit transaction"

    return ft.View(
        controls=[
            ft.Container(
                alignment=ft.alignment.top_left,
                expand=True,
                padding=ft.padding.only(left=10),
                bgcolor=ft.colors.WHITE70,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(transaction_view_headline, size=18, color=ft.colors.BLUE_600,
                                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                                ft.IconButton(
                                    icon=ft.icons.CLOSE,
                                    on_click=back_button_callable
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        SegmentButton(transaction_pipe.transaction).get(),
                        ft.Divider(leading_indent=20, trailing_indent=20),
                        TransactionInputSection(page, transaction_pipe).get(),
                        ft.Divider(leading_indent=20, trailing_indent=20),
                    ],
                    spacing=0,
                ),
            )

        ],
        bgcolor=ft.colors.WHITE,
        bottom_appbar=transaction_view_appbar.get(),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        floating_action_button=ft.FloatingActionButton(
            icon=ft.icons.CHECK,
            bgcolor=ft.colors.AMBER_300,
            shape=ft.RoundedRectangleBorder(radius=40),
            scale=1,
            on_click=save_transaction_button_callable,
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,
    )
