from typing import Callable

import flet as ft

from xpense.types import Transaction

DEFAULT_EXPENSE_CATEGORIES_WITH_ICONS = {
    "grocery": ft.icons.LOCAL_GROCERY_STORE,
    "transportation": ft.icons.DIRECTIONS_CAR,
    "restaurant": ft.icons.RESTAURANT,
    "healthcare": ft.icons.MEDICAL_SERVICES,
    "entertainment": ft.icons.WEEKEND,
    "clothing": ft.icons.SHOPPING_BAG_OUTLINED,
    "travel": ft.icons.AIRPLANE_TICKET,
    "education": ft.icons.SCHOOL,
    "medical": ft.icons.MEDICAL_SERVICES,
    "housing": ft.icons.HOME,
    "shopping": ft.icons.SHOP,
    "technology": ft.icons.BIOTECH,
    "car": ft.icons.LOCAL_CAR_WASH,
    "rent": ft.icons.HOUSE,
    "mortgage": ft.icons.HOME_REPAIR_SERVICE,
    "pets": ft.icons.PETS,
    "car lease": ft.icons.CAR_RENTAL,
    "personal loan": ft.icons.PERSON_ADD,
    "business": ft.icons.BUSINESS,
    "investments": ft.icons.BUSINESS_CENTER,
    "donations": ft.icons.HIVE,
    "gifts": ft.icons.CARD_GIFTCARD,
    "lending": ft.icons.MONETIZATION_ON,
    "other": ft.icons.OTHER_HOUSES,
}


def create_category_container(category_name: str, icon_name: ft.icons, on_click_func: Callable) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon_name, size=40),
                ft.Text(category_name.title(), size=20),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        on_click=on_click_func,
        data=category_name,
        height=60,
    )


class ExpenseCategoryButton:
    def __init__(self, page: ft.Page, category_label_ref: ft.Ref[ft.Text], transaction: Transaction):
        self._page = page
        self._category_label_ref = category_label_ref
        self._transaction = transaction

        self._click_category = lambda event: self.on_click_category(event)
        self._dialog_modal = ft.AlertDialog(
            modal=True,
            content=self._get_content(),
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.BeveledRectangleBorder(),
            title_padding=ft.padding.symmetric(20, 24),
            content_padding=ft.padding.symmetric(0, 0),
            inset_padding=ft.padding.symmetric(50, 50),
            bgcolor=ft.colors.WHITE,
        )

    def open_dialog(self, _: ft.ControlEvent):
        self._page.open(self._dialog_modal)

    def on_click_category(self, event: ft.ControlEvent):
        self._category_label_ref.current.value = event.control.data.capitalize()
        self._transaction.category = event.control.data
        self._page.close(self._dialog_modal)
        self._page.update()

    def _get_content(self):
        return ft.ListView(
            spacing=0,
            controls=[
                create_category_container(name, icon, self._click_category)
                for name, icon in DEFAULT_EXPENSE_CATEGORIES_WITH_ICONS.items()
            ]
        )
