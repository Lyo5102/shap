import json

from fastapi.responses import RedirectResponse
from nicegui import app, ui

from defs import sessions_file, login_file
from download import setup_download_page
from end import setup_end_page
from question import setup_question_page
from read_login_file import read_login_file


class SessionParams:
    def __init__(self):
        with open(sessions_file()) as f:
            self.sessions = json.load(f)

        self.p_id = ""
        self.section = ""

    def valid_session(self):
        return str(self.section) in self.sessions

    def get_session(self):
        section = str(self.section)
        return self.sessions[section]

@ui.page("/")
def index_page() -> None:

    session = SessionParams()
    
    def start_session_clicked():
        if session.valid_session():
            setup_question_page(session.p_id, session.get_session(), session.section)
            ui.navigate.to(f"/question-{session.section}")

        else:
            ui.notify("Invalid session", type="negative")

    with ui.column().classes("w-full items-center"):
        ui.input(label="被験者ID", placeholder="Please input subject ID").bind_value(
            session, "p_id"
        )
        ui.space()
        ui.label("Session").style("font-size: 1.5em") 
        ui.toggle([1,2,3], value=1).bind_value(session, "section")
        ui.button("Start session", on_click=start_session_clicked)


#@ui.page("/")
def login() -> None:
    passwords = read_login_file(login_file())

    def try_login() -> None:
        if passwords.get(username.value) == password.value:
            app.storage.user.update({"username": username.value, "authenticated": True})
            setup_session_page(username.value)
            ui.navigate.to("/session")
        else:
            ui.notify("Wrong username or password", color="negative")

    if app.storage.user.get("authenticated", False):
        setup_session_page("False")
    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on("keydown.enter", try_login)
        password = ui.input("Password", password=True, password_toggle_button=True).on(
            "keydown.enter", try_login
        )
        ui.button("Log in", on_click=try_login)


setup_end_page()
setup_download_page()
ui.run(
    host="0.0.0.0",
    port=8080,
    title="Which Face is Fake?",
    storage_secret="private key to secure the browser session cookie",
)
