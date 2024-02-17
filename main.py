import datetime
import pathlib

import flet as ft
import flet_route

from bugbro.actions import get_navigator
from bugbro.components.layout.app_bar import get_app_bar
from bugbro.components.layout.navigation_bar import get_navigation_bar
from bugbro.types import Routes
from bugbro.views.calendar.controls import get_calendar_controls
from bugbro.views.household.controls import get_household_controls
from bugbro.views.view_builder import get_view


def main(page: ft.Page):
    page.title = "BugBro - Budgeting Simplified"

    # Only temporary vars.
    page.window_width = 400
    page.window_height = 700
    # page.window_frameless = True

    # Common variables.
    current_date = datetime.date.today()

    # Common layout.
    navigator = get_navigator(page)

    app_bar = get_app_bar()
    page.appbar = app_bar
    navigation_bar = get_navigation_bar(navigator)
    page.navigation_bar = navigation_bar

    # Build application views.
    flet_route_main_view = get_view(route_url="/", controls=get_household_controls(current_date))
    flet_route_household_view = get_view(route_url=f"/{Routes.HOUSEHOLD.value.lower()}",
                                         controls=get_household_controls(current_date))
    flet_route_calendar_view = get_view(route_url=f"/{Routes.CALENDAR.value.lower()}",
                                        controls=get_calendar_controls(page, current_date))

    # Build application routing.
    index_router = flet_route.path(
        url="/",
        clear=True,
        view=flet_route_main_view
    )

    household_router = flet_route.path(
        url=f"/{Routes.HOUSEHOLD.value.lower()}",
        clear=True,
        view=flet_route_household_view
    )

    calendar_router = flet_route.path(
        url=f"/{Routes.CALENDAR.value.lower()}",
        clear=True,
        view=flet_route_calendar_view
    )

    app_routes = [
        index_router,
        household_router,
        calendar_router
    ]
    flet_route.Routing(page, app_routes=app_routes, appbar=app_bar, navigation_bar=navigation_bar)

    page.go(page.route)
    page.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="bugbro/assets/")
