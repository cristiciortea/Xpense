import flet as ft

from flet_core import ControlEvent


def get_navigator(page: ft.Page):
    def change_tab(event: ControlEvent):
        destination = page.navigation_bar.destinations[event.control.selected_index]
        page.appbar.title = ft.Text(destination.label)
        page.go(f"/{destination.label.lower()}")
        page.update()

    return change_tab
