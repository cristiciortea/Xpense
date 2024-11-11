from typing import List, Optional

import flet as ft


def transaction_row_build(controls: List[ft.Control]):
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=controls,
        spacing=0
    )
