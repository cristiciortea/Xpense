from typing import List, Optional

import flet as ft


def transaction_container_build(controls: List[ft.Control], height: Optional[int] = None):
    return ft.Container(
        alignment=ft.alignment.center_left,
        height=height,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=controls,
            spacing=0
        ),
    )
