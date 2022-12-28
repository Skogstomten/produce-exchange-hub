import sys
import subprocess

subdirs = ["authentication", "farmers_market", "main"]


def _run_django_admin_command(commands, working_dir):
    process = subprocess.run(
        ["django-admin.exe"] + commands,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=working_dir,
    )
    print(process.stdout)


def make_messages(subdir):
    print(f"Making messages for {subdir}")
    _run_django_admin_command(["makemessages", "--all"], subdir)


def compile_messages(subdir):
    print(f"Compiling messages for {subdir}")
    _run_django_admin_command(["compilemessages"], subdir)


def for_each_subdir(func):
    for subdir in subdirs:
        func(subdir)


commands = {
    "makemessages": (for_each_subdir, (make_messages,)),
    "compilemessages": (for_each_subdir, (compile_messages,)),
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing command")
    else:
        command = sys.argv[1].lower()
        try:
            func, args = commands[command]
            func(*args)
        except KeyError:
            print("Unsupported command. Supported commands are: {}".format(", ".join([k for k in commands.keys()])))
