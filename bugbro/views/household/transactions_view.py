import datetime
from typing import Callable, List

import flet as ft

from bugbro.views.household.category_button import CategoryButton
from bugbro.views.household.common.transaction_container import transaction_container_build


class SegmentButton:
    def __init__(self):
        pass

    def _get_segment_button(self) -> ft.SegmentedButton:
        return ft.SegmentedButton(
            on_change=lambda _: print("Segment change"),
            width=360,
            selected={"Income"},
            expand_loose=False,
            expand=True,
            segments=[
                ft.Segment(
                    value="Income",
                    label=ft.Text("Income"),
                ),
                ft.Segment(
                    value="Expense",
                    label=ft.Text("Expense"),
                ),
                ft.Segment(
                    value="Allocation",
                    label=ft.Text("Allocation"),
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


class Transaction:
    def __init__(self, page: ft.Page, current_date: datetime.date):
        self._page = page
        self._current_date = current_date

        self._transaction_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
        self._amount = 0
        self._selected_category = "Default"

        self._date_picker = ft.DatePicker(
            on_change=lambda _: self._on_date_change(self._date_picker.value),
            first_date=datetime.datetime.combine(self._current_date - datetime.timedelta(days=365), datetime.time()),
        )
        self._page.overlay.append(self._date_picker)
        self._category_modal = CategoryButton(self._page)

    def _on_date_change(self, target_date: datetime.datetime):
        self._transaction_date = datetime.datetime.combine(target_date, datetime.datetime.now().time()).strftime(
            '%Y-%m-%d %H:%M:%S')
        print(self._transaction_date)

    def _on_text_field_change(self, event):
        self._amount = event.control.value

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
                        ft.TextField(
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
                        )
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
    return ft.View(
        controls=[
            ft.Container(
                alignment=ft.alignment.top_left,
                expand=True,
                bgcolor=ft.colors.WHITE70,
                # margin=-10,
                content=ft.Column(
                    controls=[
                        ft.Text("Add transaction", size=18, color=ft.colors.BLUE_600,
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                        SegmentButton().get(),
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
