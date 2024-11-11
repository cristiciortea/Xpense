import datetime

import flet as ft
import flet_route

from xpense.actions import get_navigator
from xpense.components.layout.app_bar import get_app_bar
from xpense.components.layout.navigation_bar import get_navigation_bar
from xpense.types import Routes
from xpense.views.calendar.controls import get_calendar_controls
from xpense.views.household.controls import get_household_controls
from xpense.views.view_builder import get_view


def main(page: ft.Page):
    page.title = "Xpense - Expense tracker & budgeting simplified"

    # Only temporary vars.
    page.window.width = 400
    page.window.height = 700
    # page.window_frameless = True

    # Common variables.
    current_date = datetime.date.today()
    data_aggregation = ft.Ref[ft.Text]()

    # Common layout.
    navigator = get_navigator(page)
    app_bar = get_app_bar()
    page.appbar = app_bar
    navigation_bar = get_navigation_bar(navigator)
    page.navigation_bar = navigation_bar

    # Build application views.
    flet_route_main_view = get_view(route_url="/",
                                    controls=get_household_controls(current_date, data_aggregation, page))
    flet_route_household_view = get_view(route_url=f"/{Routes.HOUSEHOLD.value.lower()}",
                                         controls=get_household_controls(current_date, data_aggregation, page))
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
        calendar_router,
    ]
    flet_route.Routing(page, app_routes=app_routes, appbar=app_bar, navigation_bar=navigation_bar)

    page.go(page.route)
    page.update()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="xpense/assets")
