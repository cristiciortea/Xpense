from typing import Callable

import flet as ft

from xpense.types import Transaction, TransactionType

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
    "fitness": ft.icons.FITNESS_CENTER,
    "technology": ft.icons.BIOTECH,
    "car": ft.icons.LOCAL_CAR_WASH,
    "rent": ft.icons.HOUSE,
    "mortgage": ft.icons.HOME_REPAIR_SERVICE,
    "pets": ft.icons.PETS,
    "insurance": ft.icons.INTERESTS,
    "car lease": ft.icons.CAR_RENTAL,
    "personal loan": ft.icons.PERSON_ADD,
    "business": ft.icons.BUSINESS,
    "investments": ft.icons.BUSINESS_CENTER,
    "donations": ft.icons.HIVE,
    "gifts": ft.icons.CARD_GIFTCARD,
    "lending": ft.icons.MONETIZATION_ON,
    "other": ft.icons.OTHER_HOUSES,
}

DEFAULT_INCOME_CATEGORIES_WITH_ICONS = {
    "salary": ft.icons.MONETIZATION_ON,
    "business": ft.icons.BUSINESS,
    "loan": ft.icons.PERSON_ADD,
    "insurance": ft.icons.INTERESTS,
    "rent": ft.icons.HOUSE,
    "investments": ft.icons.BUSINESS_CENTER,
    "donations": ft.icons.HIVE,
    "child support": ft.icons.CHILD_CARE,
    "childcare leave benefits": ft.icons.CHILD_FRIENDLY,
    "tip": ft.icons.TIPS_AND_UPDATES,
    "bonus": ft.icons.CABIN_SHARP,
    "overtime": ft.icons.SETTINGS_OVERSCAN_ROUNDED,
    "retirement": ft.icons.SPORTS_FOOTBALL,
    "government benefits": ft.icons.MONEY_OFF_SHARP,
    "passive income": ft.icons.INCOMPLETE_CIRCLE,
    "scholarship": ft.icons.SCHOOL,
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


class TransactionCategoryButton:
    def __init__(self, page: ft.Page, category_label_ref: ft.Ref[ft.Text], transaction: Transaction):
        self._page = page
        self._category_label_ref = category_label_ref
        self._transaction = transaction

        self._click_category = lambda event: self.on_click_category(event)
        self._dialog_modal = ft.AlertDialog(
            modal=False,  # Whether dialog can be dismissed/closed by clicking the area outside of it.
            content=self._get_content(self._transaction),
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.BeveledRectangleBorder(),
            title_padding=ft.padding.symmetric(20, 24),
            content_padding=ft.padding.symmetric(0, 0),
            inset_padding=ft.padding.symmetric(50, 50),
            bgcolor=ft.colors.WHITE,
            scrollable=True,
        )

    def open_dialog(self, _: ft.ControlEvent):
        self._dialog_modal.content = self._get_content(self._transaction)
        self._page.open(self._dialog_modal)

    def on_click_category(self, event: ft.ControlEvent):
        self._category_label_ref.current.value = event.control.data.capitalize()
        self._transaction.category = event.control.data
        self._page.close(self._dialog_modal)
        self._page.update()

    def _get_content(self, transaction: Transaction) -> ft.ListView:
        if transaction.type == TransactionType.INCOME:
            controls = [
                create_category_container(name, icon, self._click_category)
                for name, icon in DEFAULT_INCOME_CATEGORIES_WITH_ICONS.items()
            ]
        else:
            controls = [
                create_category_container(name, icon, self._click_category)
                for name, icon in DEFAULT_EXPENSE_CATEGORIES_WITH_ICONS.items()
            ]
        return ft.ListView(
            spacing=0,
            controls=controls
        )
