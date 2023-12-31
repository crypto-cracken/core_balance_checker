import sys
import os
import platform


class bcolors:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


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


def set_title(title):
    system_type = platform.system()
    if system_type == "Windows":
        os.system("title " + title)
    elif system_type == "Linux":
        print(f"\33]0;{title}\a", end="", flush=True)


def save_result(msg, filename, with_balance):
    if with_balance:
        print(bcolors.GREEN + msg + bcolors.END)
    else:
        print(bcolors.YELLOW + msg + bcolors.END)

    if with_balance:
        path = f"results/with_balance_{filename}.txt"
    else:
        path = f"results/no_balance_{filename}.txt"

    with open(path, "a", encoding="utf8") as f:
        f.write(f"{msg}\n")
