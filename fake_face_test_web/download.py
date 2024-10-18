from functools import partial

from fastapi.responses import RedirectResponse
from nicegui import ui, app

from defs import results_dir

# results_dir().mkdir(exist_ok=True)
app.add_static_files("/results", results_dir())  # serve all files in this folder


def setup_download_page():
    @ui.page("/download")
    def download_page() -> None:
        if not app.storage.user.get("authenticated_admin", False):
            return RedirectResponse("/adminlog")

        for f in results_dir().glob("*"):
            ui.button(
                f.name,
                icon="download",
                on_click=partial(ui.download, f"/results/{f.name}"),
            )

    @ui.page("/adminlog")
    def admin() -> None:
        def admin_login() -> None:
            if adminpass.value == "cpsexperiment20238025":
                app.storage.user.update({"authenticated_admin": True})
                ui.open("/download")
            else:
                ui.notify("Wrong password", color="negative")

        if app.storage.user.get("authenticated_admin", False):
            return RedirectResponse("/download")
        with ui.card().classes("absolute-center"):
            adminpass = ui.input(
                "Password", password=True, password_toggle_button=True
            ).on("keydown.enter", admin_login)
            ui.button("Log in", on_click=admin_login)
