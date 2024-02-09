import flet as ft


def main(page: ft.Page):
    page.title = "BugBro - Budgeting Simplified"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    greeting = ft.Text("Welcome to BugBro!", size=20, weight="bold")
    page.add(greeting)


if __name__ == "__main__":
    ft.app(target=main)
