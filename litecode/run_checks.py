# LiteCode is a lightweight Python stack for accelerated development of applications and services
#
# Though Litecode, "Single" is the new "Full" stack. Using FastAPI and NiceGUI to build
# web applications entirely on the server side, Litecode removes the need for client-side
# JavaScript or TypeScript, while complexity is reduced by using a simplified architecture
# and single language for the entire stack.
#
# License: MIT License
# For the full license text, please refer to the LICENSE file in the root of the project.
#
# Copyright (c) 2024 Iwan van der Kleijn


import subprocess


def run_checks() -> None:
    commands = [
        ["black", "litecode"],
        ["flake8", "litecode"],
        ["mypy", "litecode"],
        ["pytest"],
    ]

    for command in commands:
        result = subprocess.run(command)
        if result.returncode != 0:
            print(f"Command {command} failed with return code {result.returncode}")
            break  # Stop running the next commands if one fails


if __name__ == "__main__":
    run_checks()
