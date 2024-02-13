import flet_route

from bugbro.types import Routes
from bugbro.views.view_builder import flet_route_main_view, flet_route_household_view, flet_route_calendar_view

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
