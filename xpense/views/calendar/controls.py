import calendar
import datetime
from typing import List, Optional, Callable, Tuple

import flet as ft
from flet_core import IconButton

from xpense.utilities.calendar import get_sign
from xpense.views.calendar.components import get_header_current_day_button, get_header_calendar_icon


class CalendarBuilder:
    def __init__(self, start_date: Optional[datetime.date] = None):
        if start_date is None:
            self._start_date = datetime.date.today()
        else:
            self._start_date = start_date
        self._current_year = self._start_date.year
        self._current_year_backup = self._start_date.year
        self._current_month = self._start_date.month
        self._current_month_backup = self._start_date.month

        self._date_clicks: List[ft.Container] = []

        self._calendar_grid: Optional[ft.Column] = None

    def _build_calendar_grid(self):
        if self._calendar_grid:
            return

        self._calendar_grid = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _reset_calendar_grid_controls(self):
        self._calendar_grid.controls = []

    def _get_navigation_buttons(self) -> tuple[IconButton, IconButton]:
        before_button = PaginationButton(
            "before",
            lambda event: self.shift(months=-1)
        ).build()
        next_button = PaginationButton(
            "next",
            lambda event: self.shift(months=1)
        ).build()
        return before_button, next_button

    def _get_month_label(self) -> ft.Container:
        return ft.Container(width=115,content=ft.Text(
            f"{calendar.month_name[self._current_month]} {self._current_year}",
            size=14,
            weight=ft.FontWeight.BOLD,
        ))

    def _get_basic_month_grid(self, month_label: ft.Container) -> ft.Container:
        before_button, next_button = self._get_navigation_buttons()
        return ft.Container(
            content=ft.Row(
                controls=[before_button, month_label, next_button],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            alignment=ft.alignment.center,
            height=50,
        )

    @staticmethod
    def _get_weekday_labels() -> List[ft.Container]:
        return [
            ft.Container(
                width=28,
                height=28,
                alignment=ft.alignment.center,
                content=ft.Text(
                    weekday,
                    size=12,
                    color=ft.colors.BLACK54,
                )
            ) for weekday in tuple(calendar.day_abbr)
        ]

    def _build_calendar(self) -> None:
        self._build_calendar_grid()
        self._reset_calendar_grid_controls()

        # This is the label that goes at the top of the
        # weekday labels.
        month_label = self._get_month_label()
        month_grid = self._get_basic_month_grid(month_label)
        self._calendar_grid.controls.append(month_grid)

        # Build the weekday row which is singular, and it looks like
        # Mon Tue Wed Thu Fri Sat Sun.
        weekday_labels = self._get_weekday_labels()
        weekday_row = ft.Row(
            controls=weekday_labels,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self._calendar_grid.controls.append(weekday_row)

        # Add the week containers with each day of the month
        # to the root calendar grid.
        month_matrix = calendar.monthcalendar(self._current_year, self._current_month)
        for week in month_matrix:
            week_container = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            for day in week:
                day_container = self._get_day_container(day)
                day_label = ft.Text(str(day), size=12) if day != 0 else None
                day_container.content = day_label

                if (
                        day == self._start_date.day and
                        self._current_month == self._start_date.month and
                        self._current_year == self._start_date.year
                ):
                    day_container.bgcolor = ft.colors.TEAL_700

                week_container.controls.append(day_container)
            self._calendar_grid.controls.append(week_container)

    def get(self):  # -> ft.Column:
        self._build_calendar()
        return ft.Container(
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.AMBER_100,
            height=345,
            content=self._calendar_grid,
        )

    def _sync_current_dates(self) -> None:
        self._current_year_backup = self._current_year
        self._current_month_backup = self._current_month

    def _calendar_needs_reset(self) -> bool:
        return self._current_year != self._current_year_backup or self._current_month != self._current_month_backup

    def reset_calendar(self) -> None:
        if self._calendar_needs_reset():
            self._build_calendar()
            self._calendar_grid.update()
            self._date_clicks = []
            self._sync_current_dates()

    @staticmethod
    def _get_relative_delta(months: int) -> Tuple[int, int]:
        if not isinstance(months, int):
            raise TypeError("months should be integers.")
        sign = get_sign(months)
        div, mod = divmod(months * sign, 12)
        relative_months = mod * sign
        relative_years = div * sign
        return relative_months, relative_years

    def shift(self, years: Optional[int] = 0, months: Optional[int] = 0) -> None:
        if not isinstance(years, int) or not isinstance(months, int):
            raise TypeError("years and months should be integers.")

        if abs(months) > 11:
            relative_months, relative_years = self._get_relative_delta(months)
            months = relative_months
            years += relative_years

        if months:
            self.set_current_month(self._current_month + months)

        if years:
            self.set_current_year(self._current_year + years)

        self.reset_calendar()

    def set_current_month(self, month: int) -> None:
        if 1 <= month <= 12:
            self._current_month = month
        elif month > 12 or month <= 0:
            relative_months, relative_years = self._get_relative_delta(month)
            self.set_current_month(relative_months if relative_months != 0 else 12)
            relative_years = relative_years if relative_years != 0 else -1
            self.set_current_year(self._current_year + relative_years)
        self.reset_calendar()

    def set_current_year(self, year: int) -> None:
        if year > 0:
            self._current_year = year
        self.reset_calendar()

    def go_today(self) -> None:
        self.set_current_year(self._start_date.year)
        self.set_current_month(self._start_date.month)
        self.highlight_day(self._start_date.day)

    def highlight_day(self, target_day: int) -> None:
        for week_control in self._calendar_grid.controls:
            for day_control in week_control.controls:
                if day_control.data == target_day:
                    day_control: ft.Container
                    self._click_date(ft.ControlEvent(control=day_control, target="", name="", data="", page=""))

    def pick_date(self, target_date: datetime.datetime) -> None:
        self.set_current_month(target_date.month)
        self.set_current_year(target_date.year)
        self.highlight_day(target_date.day)

    def _click_date(self, event: ft.ControlEvent) -> None:
        clicked_date = event.control

        # Determine color based on the date
        def target_color(date):
            is_current_date = int(date.content.value) == self._start_date.day
            return ft.colors.TEAL_700 if is_current_date else ft.colors.WHITE

        # Toggle or set color for clicked date
        if self._date_clicks and clicked_date == self._date_clicks[0]:
            # Toggle if same date clicked again
            new_color = ft.colors.BLUE_600 if clicked_date.bgcolor != ft.colors.BLUE_600 else target_color(clicked_date)
        else:
            # Reset previous date's color if different date clicked
            if self._date_clicks:
                self._date_clicks[0].bgcolor = target_color(self._date_clicks[0])
                self._date_clicks[0].update()

            new_color = ft.colors.BLUE_600
            # Update or set the clicked date in the list
            self._date_clicks = [clicked_date]

        clicked_date.bgcolor = new_color
        clicked_date.update()

    def _get_day_container(self, day: int) -> ft.Container:
        if day == 0:
            return ft.Container(
                width=28,
                height=28
            )
        else:
            return ft.Container(
                width=28,
                height=28,
                border=ft.border.all(0.5, ft.colors.BLACK54),
                alignment=ft.alignment.center,
                data=day,
                on_click=lambda event: self._click_date(event),
                animate=150
            )


class PaginationButton:
    def __init__(self, text: str, func: Callable):
        self.text = text
        self.func = func

    def build(self) -> ft.IconButton:
        if self.text.lower() == "next":
            icon = ft.icons.NAVIGATE_NEXT_SHARP
        elif self.text.lower() == "before":
            icon = ft.icons.NAVIGATE_BEFORE_SHARP
        else:
            raise NameError(f"Unknown text type: {self.text}. Use 'next' or 'before'.")

        return ft.IconButton(
            icon=icon,
            width=56,
            height=38,
            on_click=self.func,
            style=ft.ButtonStyle(
                # shape=ft.RoundedRectangleBorder(radius=6),
                bgcolor=ft.colors.TRANSPARENT
            ),
        )


class CalendarNavigator:
    def __init__(self, page: ft.Page, start_date: Optional[datetime.date] = None):
        if start_date is None:
            self.start_date = datetime.date.today()
        else:
            self.start_date = start_date

        self.calendar_builder = CalendarBuilder(self.start_date)

        self.header_text = ft.Text(
            value=self.start_date.strftime("%B %d, %Y"),
            width=225,
            size=15,
            color=ft.colors.BLACK54,
            weight=ft.FontWeight.W_400
        )

        self.calendar_container: ft.Container | None = None

        self.page = page

    def _get_calendar_container(self) -> ft.Container:
        if self.calendar_container is None:
            self.calendar_container = ft.Container(
                height=450,
                bgcolor=ft.colors.TRANSPARENT,
                animate=300,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                alignment=ft.alignment.top_left,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        self._get_calendar_header(),
                        self.calendar_builder.get(),
                    ]
                )
            )
        return self.calendar_container

    def _toggle_calendar_expansion(self, _: ft.ControlEvent) -> None:
        if self.calendar_container.height == 47:
            self.calendar_container.height = 450
        else:
            self.calendar_container.height = 47
        self.calendar_container.update()

    def _get_header_right_side(self) -> ft.Row:
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.alignment.center_right,
            width=100,
            spacing=0,
            controls=[
                ft.Container(
                    height=36,
                    border=ft.border.only(left=ft.BorderSide(0.9, ft.colors.BLACK26)),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(right=7)
                ),
                get_header_current_day_button(
                    self.start_date.day,
                    lambda _: self.calendar_builder.go_today()
                ),
                get_header_calendar_icon(self.page, self.calendar_builder.pick_date)
            ]
        )

    def _get_calendar_header(self):
        return ft.Container(
            on_click=lambda event: self._toggle_calendar_expansion(event),
            height=47,
            bgcolor=ft.colors.GREY_50,
            padding=ft.padding.only(left=15, right=5),
            alignment=ft.alignment.center,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.header_text,
                    self._get_header_right_side()
                ]
            ),
        )

    def get(self) -> ft.Column:
        return ft.Column(
            spacing=0,
            controls=[
                self._get_calendar_container(),
            ],
        )


def get_main_container(page: ft.Page, start_date: datetime.date) -> ft.Container:
    calendar_navigator = CalendarNavigator(page, start_date)

    return ft.Container(
        alignment=ft.alignment.top_left,
        expand=True,
        padding=0,
        margin=0,
        bgcolor=ft.colors.WHITE70,
        content=ft.Column(
            controls=[
                calendar_navigator.get()
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        )
    )


def get_calendar_controls(page: ft.Page, start_date: datetime.date) -> List[ft.Control]:
    return [
        get_main_container(page, start_date)
    ]
