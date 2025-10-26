#!/usr/bin/env python3
import subprocess
import sys
import secrets
import os
import re
from typing import Mapping, Optional

PROJECT_NAME = "proxy_server"

def generate_clear_password():
    return secrets.token_hex(32)


_env_pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def replace_env_vars(
        text: str,
        env: Optional[Mapping[str, str]] = None,
        required: bool = True,
        missing_value: Optional[str] = None
) -> str:
    if env is None:
        env = os.environ

    def _repl(match: re.Match) -> str:
        var = match.group(1)
        if var in env:
            return str(env[var])
        if required:
            raise KeyError(f"Environment variable '{var}' is not set")
        # not required: use missing_value (could be None -> "None")
        return "" if missing_value is None else str(missing_value)

    return _env_pattern.sub(_repl, text)


def parse_args(argv):
    args = {}
    key = None
    for item in argv:
        if item.startswith("--"):
            key = item.lstrip("-")
            args[key] = True  # default if no value provided
        elif key:
            args[key] = item
            key = None
    return args


def up():
    """Start docker compose services"""
    subprocess.run(["docker", "compose", "-p", PROJECT_NAME, "up", "-d"], check=True)

def down():
    """Stop docker compose services and remove volumes"""
    subprocess.run(["docker", "compose", "-p", PROJECT_NAME, "down", "-v"], check=True)


class ComposeApp:

    def __init__(self, action, email,dns_token):
        self.action = action
        self.env_variables = {
            'EMAIL': email,
            'HETZNER_API_KEY':dns_token
        }

    def configure(self):
        with open('.env', 'w+') as env_file:
            for key, value in self.env_variables.items():
                env_file.write(f"{key}={value}")
                env_file.write("\n")

    def deploy(self):
        if self.action == "up":
            up()
        elif self.action == "down":
            down()
        else:
            print(f"Unknown command: {self.action}")
            print("Available commands: up, down")
            sys.exit(1)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    print(args)
    app = ComposeApp(
        action=args.get("action"),
        email=args.get("email"),
        dns_token=args.get("dns_token"),
    )

    app.deploy()
