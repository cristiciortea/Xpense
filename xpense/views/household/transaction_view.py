import dataclasses
import datetime
from typing import Callable, Optional

import flet as ft

from xpense.types import TransactionType, Transaction
from xpense.utilities.calendar import convert_datetime_to_string
from xpense.utilities.household import keep_first_dot
from xpense.views.household.expense_category_button import ExpenseCategoryButton


class SegmentButton:
    def __init__(self, transaction: Transaction):
        self._transaction = transaction
        self._transaction.type = TransactionType.get_transaction_type(TransactionType.EXPENSE.value)

    def _on_change(self, event: ft.ControlEvent):
        self._transaction.type = TransactionType.get_transaction_type(next(iter(event.control.selected)))

    def _get_segment_button(self) -> ft.SegmentedButton:
        return ft.SegmentedButton(
            on_change=lambda event: self._on_change(event),
            width=380,
            selected={TransactionType.EXPENSE.value},
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


class TransactionSection:
    def __init__(self, page: ft.Page, transaction_pipe: "TransactionPipe"):
        self._page = page
        self._transaction_pipe = transaction_pipe
        self._transaction_pipe.transaction_section = self
        self._transaction = self._transaction_pipe.transaction

        self._current_date = self._transaction.date
        self.amount_text_field: None | ft.TextField = None
        self.main_container: None | ft.Container = None
        self.amount_container: None | ft.Container = None

        self._date_picker = ft.DatePicker(
            on_change=lambda _: self._on_date_change(self._date_picker.value),
            first_date=datetime.datetime.combine(self._current_date - datetime.timedelta(days=365), datetime.time()),
        )
        self._page.overlay.append(self._date_picker)

        self._transaction.category = "Default"
        self._category_label_ref = ft.Ref[ft.Text]()
        self._category_button = ExpenseCategoryButton(self._page, self._category_label_ref, self._transaction)

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

    def _build_input_amount_text_field(self) -> ft.TextField:
        if self.amount_text_field is None:
            self.amount_text_field = ft.TextField(
                value="",
                hint_text="0.00",
                adaptive=True,
                on_change=lambda event: self._on_text_field_change(event),
                border=ft.InputBorder.NONE,
                width=80,
                height=49,
                multiline=False,
                max_lines=1,
                text_align=ft.TextAlign.END,
                text_vertical_align=ft.VerticalAlignment.START,
                keyboard_type=ft.KeyboardType.PHONE,
                text_size=13.8,
                # fill_color=ft.colors.BLUE_600
            )
        return self.amount_text_field

    def get_date_row(self) -> ft.Container:
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

    def get_amount_row(self) -> ft.Container:
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
                                ft.Icon(ft.icons.EURO_SYMBOL_OUTLINED, size=15),
                                self._build_input_amount_text_field(),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            # alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            # spacing=1,
                        )

                    ],
                    spacing=0
                )
            )
        return self.amount_container

    def get_category_row(self) -> ft.Container:
        return ft.Container(
            # bgcolor=ft.colors.BLUE,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Category", weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            ft.Text(self._transaction.category, ref=self._category_label_ref),
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
                    self.get_date_row(),
                    self.get_amount_row(),
                    self.get_category_row(),
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
    transaction_section: Optional[TransactionSection] = None


def get_transactions_view(
        page: ft.Page,
        back_button_callable: Callable,
        save_button_callable: Callable,
        transaction_pipe: TransactionPipe
) -> ft.View:
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
                                ft.Text("Add transaction", size=18, color=ft.colors.BLUE_600,
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
                        TransactionSection(page, transaction_pipe).get(),
                        ft.Divider(leading_indent=20, trailing_indent=20),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    on_click=back_button_callable
                                ),
                                ft.IconButton(
                                    icon=ft.icons.CHECK,
                                    on_click=save_button_callable
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ],
                    spacing=0,
                )
            )

        ],
        bgcolor=ft.colors.WHITE,
    )
