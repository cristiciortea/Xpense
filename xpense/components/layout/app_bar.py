import flet as ft

from xpense.types import Routes


def get_app_bar() -> ft.AppBar:
    return ft.AppBar(
        title=ft.Text(value=Routes.HOUSEHOLD.value),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        elevation=100,
        elevation_on_scroll=100,
        # force_material_transparency=True,
        # toolbar_opacity=1,
    )
