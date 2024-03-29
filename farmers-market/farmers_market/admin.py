import sys
import subprocess

SUB_DIRS = ["authentication", "farmers_market", "main"]
LINE_LENGTH = 120


def run_subprocess(arguments: list, working_dir: str | None = None):
    print(f"Running command: {' '.join(arguments)}")
    process = subprocess.run(
        arguments,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=working_dir,
    )
    print(process.stdout)


def run_django_admin_command(arguments, working_dir):
    run_subprocess(["django-admin.exe"] + arguments, working_dir)


def run_black():
    run_subprocess(["black", "./", f"--line-length={LINE_LENGTH}"])


def commit_all_changes(*messages):
    run_subprocess(["git", "add", "-A"])
    run_subprocess(["git", "commit"] + [f'-m"{message}"' for message in messages])


def make_messages(subdir):
    print(f"Making messages for {subdir}")
    run_django_admin_command(["makemessages", "--all"], subdir)


def compile_messages(subdir):
    print(f"Compiling messages for {subdir}")
    run_django_admin_command(["compilemessages"], subdir)


def for_each_subdir(function):
    for subdir in SUB_DIRS:
        function(subdir)


def format_and_commit(*messages):
    run_black()
    commit_all_changes(*messages)


commands = {
    "makemessages": (for_each_subdir, (make_messages,)),
    "compilemessages": (for_each_subdir, (compile_messages,)),
    "commit": (format_and_commit, ()),
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing command")
    else:
        command = sys.argv[1].lower()
        additional_arguments = sys.argv[2:]
        try:
            func, args = commands[command]
            func(*args, *additional_arguments)
        except KeyError:
            print("Unsupported command. Supported commands are: {}".format(", ".join([k for k in commands.keys()])))
