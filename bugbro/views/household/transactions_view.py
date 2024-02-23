import datetime
from typing import Callable, List

import flet as ft

from bugbro.types import TransactionType
from bugbro.utilities.household import keep_first_dot, add_commas_to_number_text
from bugbro.views.household.category_button import CategoryButton
from bugbro.views.household.common.transaction_container import transaction_container_build


class SegmentButton:
    def __init__(self, segment_ref: ft.Ref[ft.SegmentedButton]):
        self._segment_ref = segment_ref

    def _on_change(self, event: ft.ControlEvent):
        print("Segment change", event.control)
        print(self._segment_ref.current.selected)

    def _get_segment_button(self) -> ft.SegmentedButton:
        return ft.SegmentedButton(
            on_change=lambda event: self._on_change(event),
            width=360,
            selected={TransactionType.INCOME.value},
            expand_loose=False,
            expand=True,
            segments=[
                ft.Segment(
                    value=TransactionType.INCOME.value,
                    label=ft.Text(TransactionType.INCOME.value),
                ),
                ft.Segment(
                    value=TransactionType.EXPENSE.value,
                    label=ft.Text(TransactionType.EXPENSE.value),
                ),
                ft.Segment(
                    value=TransactionType.ALLOCATION.value,
                    label=ft.Text(TransactionType.ALLOCATION.value),
                ),
            ],
            scale=0.9,
            ref=self._segment_ref
        )

    def get(self) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.center,
            content=self._get_segment_button(),
            padding=ft.padding.only(top=25, bottom=15)
        )


class Transaction:
    def __init__(self, page: ft.Page, current_date: datetime.date):
        self._page = page
        self._current_date = current_date

        self._transaction_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
        self._amount = 0
        self._amount_text_field: None | ft.TextField = None
        self._amount_text_field_ref = ft.Ref[ft.TextField]()

        self._date_picker = ft.DatePicker(
            on_change=lambda _: self._on_date_change(self._date_picker.value),
            first_date=datetime.datetime.combine(self._current_date - datetime.timedelta(days=365), datetime.time()),
        )
        self._page.overlay.append(self._date_picker)

        self._selected_category = "Default"
        self._category_modal = CategoryButton(self._page)

    def _on_date_change(self, target_date: datetime.datetime):
        self._transaction_date = datetime.datetime.combine(target_date, datetime.datetime.now().time()).strftime(
            '%Y-%m-%d %H:%M:%S')
        print(self._transaction_date)

    def _on_text_field_change(self, event):
        amount = add_commas_to_number_text(str(event.control.value))
        amount = keep_first_dot(amount)

        if len(amount) > 10:
            self._amount_text_field_ref.current.value = amount[:10]
        else:
            self._amount_text_field_ref.current.value = amount

        if not amount == ".":
            self._amount = float(self._amount_text_field_ref.current.value.replace(",", "") or 0)
        self._amount_text_field.update()

    def _build_input_amount_text_field(self) -> ft.TextField:
        if self._amount_text_field is None:
            self._amount_text_field = ft.TextField(
                hint_text="0.00",
                adaptive=True,
                on_change=lambda event: self._on_text_field_change(event),
                border=ft.InputBorder.NONE,
                width=60,
                height=60,
                input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9\.]", replacement_string=""),
                multiline=False,
                max_lines=1,
                text_align=ft.TextAlign.START,
                text_vertical_align=ft.VerticalAlignment.CENTER,
                text_size=14,
                keyboard_type=ft.KeyboardType.PHONE,
                ref=self._amount_text_field_ref,
            )
        return self._amount_text_field

    def get_date_container(self) -> ft.Container:
        return transaction_container_build([
            ft.Text("Date", weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(self._transaction_date.split()[0]),
                on_click=lambda _: self._date_picker.pick_date())
        ])

    def get_amount_container(self) -> ft.Container:
        return transaction_container_build(
            [
                ft.Text("Amount", weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.EURO_SYMBOL_OUTLINED, size=15),
                        self._build_input_amount_text_field(),
                    ],
                    spacing=5,
                )

            ],
            height=60,
        )

    def get_category_container(self) -> ft.Container:
        return transaction_container_build(
            [
                ft.Text("Category", weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.Text(self._selected_category),
                        ft.IconButton(
                            icon=ft.icons.ARROW_DROP_DOWN,
                            on_click=lambda event: self._category_modal.open_dialog(event)
                        )
                    ],
                    spacing=5,
                )
            ]
        )

    def get(self) -> List[ft.Container]:
        return [
            self.get_date_container(),
            self.get_amount_container(),
            self.get_category_container()
        ]


def get_transactions_view(page: ft.Page, back_button_callable: Callable, current_date: datetime.date) -> ft.View:
    segment_button_ref = ft.Ref[ft.SegmentedButton]()
    return ft.View(
        controls=[
            ft.Container(
                alignment=ft.alignment.top_left,
                expand=True,
                bgcolor=ft.colors.WHITE70,
                content=ft.Column(
                    controls=[
                        ft.Text("Add transaction", size=18, color=ft.colors.BLUE_600,
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                        SegmentButton(segment_button_ref).get(),
                        *Transaction(page, current_date).get(),
                        ft.IconButton(
                            icon=ft.icons.ARROW_LEFT,
                            on_click=back_button_callable
                        )
                    ],
                    spacing=0,
                )
            )

        ],
        bgcolor=ft.colors.WHITE,
    )
