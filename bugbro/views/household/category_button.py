import flet as ft


class CategoryButton:
    def __init__(self, page: ft.Page):
        self._page = page

        self._click_category = lambda event: self.on_click_category(event)
        self._dialog_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Choose category:"),
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.icons.BED),
                        on_click=self._click_category,
                        border=ft.border.all(0.9, color=ft.colors.GREY),
                        data="abc",
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.BED),
                        on_click=self._click_category,
                        border=ft.border.all(0.9, color=ft.colors.GREY),
                        data="abc",
                        expand=True,
                        width=200,
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.BED),
                        on_click=self._click_category,
                        border=ft.border.all(0.9, color=ft.colors.GREY),
                        data="abc",
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.BED),
                        on_click=self._click_category,
                        border=ft.border.all(0.9, color=ft.colors.GREY),
                        data="abc",
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.BED),
                        on_click=self._click_category,
                        border=ft.border.all(0.9, color=ft.colors.GREY),
                        data="abc",
                        expand=True
                    ),
                ]
            ),
            actions=[
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            shape=ft.BeveledRectangleBorder(),
        )

    def open_dialog(self, _: ft.ControlEvent):
        self._page.dialog = self._dialog_modal
        self._dialog_modal.open = True
        self._page.update()

    def on_click_category(self, event: ft.ControlEvent):
        print(event.control.data)
        self._dialog_modal.open = False
        self._page.update()
