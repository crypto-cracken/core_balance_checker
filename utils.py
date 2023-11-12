import sys
import os


def get_run_path() -> str:
    if getattr(sys, "frozen", False):
        app_path = os.path.dirname(sys.executable)
    else:
        try:
            app_path = os.path.dirname(os.path.realpath(__file__))
        except NameError:
            app_path = os.getcwd()
    return app_path


def get_file_path(file_name) -> str:
    return os.path.join(get_run_path(), file_name)
