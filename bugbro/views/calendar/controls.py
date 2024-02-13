import calendar
import datetime
from typing import List, Optional

import flet as ft


class Calendar:
    def __init__(self):
        self.today = datetime.date.today()
        self.year = self.today.year
        self.month = self.today.month
        # self.next_month = self.month + 1

        self.clicks: List = []
        self.long_presses: List = []

        self.color = ft.colors.BLUE

        self.selected_date = None
        self.calendar_grid: ft.Column | None = None

    def build_calendar_grid(self) -> None:
        if self.calendar_grid is not None:
            return
        self.calendar_grid = ft.Column(
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def build_calendar(self) -> None:
        self.calendar_grid.controls = []
        year = self.year
        month = self.month

        month_label = ft.Text(
            f"{calendar.month_name[month]} {year}",
            size=14,
            weight=ft.FontWeight.BOLD,
        )
        month_grid = ft.Column(alignment=ft.MainAxisAlignment.CENTER)
        month_grid.controls.append(ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[month_label]
        ))

        weekday_labels = [
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
        weekday_row = ft.Row(controls=weekday_labels)
        month_grid.controls.append(weekday_row)
        self.calendar_grid.controls = [month_grid]

        month_matrix = calendar.monthcalendar(self.year, self.month)
        for week in month_matrix:
            week_container = ft.Row()
            for day in week:
                day_container = self._get_day_container(day)
                day_label = ft.Text(str(day), size=12) if day != 0 else None
                day_container.content = day_label

                if day == self.today.day and month == self.today.month and year == self.today.year:
                    day_container.bgcolor = ft.colors.TEAL_700

                week_container.controls.append(day_container)
            self.calendar_grid.controls.append(week_container)

    def build(self) -> ft.Column:
        self.build_calendar_grid()
        self.build_calendar()
        return self.calendar_grid

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
                data=self.today,
                # on_click=lambda event: self.show_date(event)
                animate=400
            )


def get_calendar_controls() -> List[ft.Control]:
    return [Calendar().build()]
