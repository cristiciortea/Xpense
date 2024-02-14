import flet as ft
import flet_route

from bugbro.actions import get_navigator
from bugbro.components.layout.app_bar import get_app_bar
from bugbro.components.layout.navigation_bar import get_navigation_bar
from bugbro.routes import app_routes


def main(page: ft.Page):
    page.title = "BugBro - Budgeting Simplified"

    # Only temporary vars.
    page.window_width = 400
    page.window_height = 700
    # page.window_frameless = True

    # Common layout.
    navigator = get_navigator(page)

    app_bar = get_app_bar()
    page.appbar = app_bar
    navigation_bar = get_navigation_bar(navigator)
    page.navigation_bar = navigation_bar

    # Routing.
    flet_route.Routing(page, app_routes=app_routes, appbar=app_bar, navigation_bar=navigation_bar)
    # page.go(page.route)
    page.go("/calendar")
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
