import flet as ft


class CategoryButton:
    def __init__(self, page: ft.Page):
        self._page = page

        self._click_category = lambda event: self.on_click_category(event)
        self._dialog_modal = ft.AlertDialog(
            modal=False,
            content=self._get_content(),
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            shape=ft.BeveledRectangleBorder(),
            title_padding=ft.padding.symmetric(20, 24),
            content_padding=ft.padding.symmetric(0, 0),
            inset_padding=ft.padding.symmetric(50, 50),
            bgcolor=ft.colors.WHITE,
        )

    def open_dialog(self, _: ft.ControlEvent):
        self._page.dialog = self._dialog_modal
        self._dialog_modal.open = True
        self._page.update()

    def on_click_category(self, _: ft.ControlEvent):
        self._dialog_modal.open = False
        self._page.update()

    def _get_content(self):
        return ft.ListView(
            spacing=0,
            controls=[
                ft.Container(
                    content=ft.Icon(ft.icons.BED),
                    on_click=self._click_category,
                    border=ft.border.only(bottom=ft.BorderSide(0.9, ft.colors.GREY)),
                    data="abc",
                    alignment=ft.alignment.center,
                    height=100,
                )
            ],
        )
