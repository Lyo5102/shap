from nicegui import ui


def setup_end_page():
    @ui.page("/end")
    def end_page() -> None:
        with ui.column().classes("w-full items-center"):
            ui.label("Thank you for your participation!").style(
                "font-size: 6em; text-align: center"
            ).tailwind.font_weight("extra bold")
