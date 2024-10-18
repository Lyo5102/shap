from pathlib import Path

module_name = "fake_face_test_web"


def module_root() -> Path:
    return Path(__file__).parent


def project_root() -> Path:
    return module_root().parent


def questions_dir() -> Path:
    return project_root() / "questions"


def sessions_file() -> Path:
    return project_root() / "sessions.json"


def login_file() -> Path:
    return project_root() / "logininfo.csv"


def images_dir() -> Path:
    return project_root() / "images"


def results_dir() -> Path:
    return project_root() / "results"
