#!/usr/bin/python3
import argparse
import os

from version import VERSION


class PrintColours:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = "\033[1;31m"
    YELLOW = "\033[1;33m"
    LIGHT_PURPLE = "\033[1;35m"
    RESET = "\u001b[0m"

# BUILD_ERRORS_PATTERN = re.compile(r"There were (\d+) build errors")

def colorize_output(output:list[str]):
    errors:list[str] = []
    warnings:list[str] = []
    errors_number:str = ""
    build_time:str = ""
    for line in output:
        if "error:" in line:
            errors.append(f"{PrintColours.RED}{line}{PrintColours.RESET}")
        elif "warning:" in line:
            warnings.append(f"{PrintColours.YELLOW}{line}{PrintColours.RESET}")
        elif "build errors" in line:
            errors_number = f"{PrintColours.RED}{line}{PrintColours.RESET}"
        elif "build time" in line:
            build_time = f"{PrintColours.LIGHT_PURPLE}{line}{PrintColours.RESET}"
        else:
            print(line)
    for line in errors:
        print(line)
    for line in warnings:
        print(line)
    print_result(errors, warnings, errors_number, build_time)

def print_result(errors:list[str], warnings:list[str], errors_number:str, build_time:str):
    if build_time:
        print("-" * 20)
        print(build_time)
    print("-" * 20)
    if errors:
        print(f"{PrintColours.RED}Build: FAILED: {errors_number}{PrintColours.RESET}")
    elif warnings:
        print(f"{PrintColours.YELLOW}Build: SUCCESS WITH WARNINGS{PrintColours.RESET}")
    else:
        print(f"{PrintColours.GREEN}Build: SUCCESS{PrintColours.RESET}")
    print("-" * 20)

def cli(*args):
    parser = argparse.ArgumentParser(prog='Coloring', description='CLI for coloring emBuild output v' + VERSION)
    parser.add_argument('-c', '--command', type=str, help='emBuild command with arguments', required=True)
    parser.add_argument('-e', '--stderr', help='Parsing only stderr', required=False, default=True, action='store_false')
    try:
        args = parser.parse_args()
    except:
        return
    only_stderr = "2>&1 1>/dev/null"
    if os.name == "nt":
        only_stderr = "2>&1 1>nul"
    redirect = only_stderr if args.stderr else "2>&1"
    embuild_output = os.popen(f"{args.command} {redirect}").read().split("\n")
    colorize_output(embuild_output)

if __name__ == "__main__":
    cli()



