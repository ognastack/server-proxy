#!/usr/bin/env python3
import subprocess
import sys
import secrets
import time

PROJECT_NAME = "proxy_server"

KONG_CONFIG = """
_format_version: "3.0"

# Admin protection
consumers:
  - username: admin
    keyauth_credentials:
      - key: ${ADMIN_API_KEY}

# Protect Kong's own Admin API via proxy
services:
  - name: admin-api
    url: http://kong-cp:8001
    routes:
      - name: admin-api-route
        paths:
          - /admin
    plugins:
      - name: key-auth

"""


def generate_clear_password():
    return secrets.token_hex(32)


import os
import re
from typing import Mapping, Optional

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


def up_prod():
    """
    Start docker compose services
    """
    subprocess.run(["docker", "compose", "-p", PROJECT_NAME, '-f', 'docker-certificates.yaml', "up", "-d"], check=True)
    time.sleep(200)
    subprocess.run(["chmod","-R" ,"755", "/etc/letsencrypt/live"], check=True)
    subprocess.run(["chmod","-R", "755", "./etc/letsencrypt/archive"], check=True)
    subprocess.run(["docker", "compose", "-p", PROJECT_NAME, "up", "-d"], check=True)

def down():
    """Stop docker compose services and remove volumes"""
    subprocess.run(["docker", "compose", "-p", PROJECT_NAME, "down", "-v"], check=True)


class ComposeApp:

    def __init__(self, action, domain, email,conf):
        self.action = action
        self.conf = conf
        self.env_variables = {
            'POSTGRES_USER': "proxy_server_user",
            'POSTGRES_PASSWORD': generate_clear_password(),
            'POSTGRES_DB': "ogna_db",
            'POSTGRES_NON_ROOT_USER': "proxy_server_user_no_root",
            'POSTGRES_NON_ROOT_PASSWORD': generate_clear_password(),
            'ENCRYPTION_KEY': generate_clear_password(),
            'KONG_ADMIN_KEY': generate_clear_password(),
            'KONG_PASSWORD': generate_clear_password(),
            'ADMIN_API_KEY': generate_clear_password(),
            'KONG_LOG_LEVEL': "notice",
            'DOMAIN': domain,
            'EMAIL': email,
        }

        if self.action == 'up-prod':
            self.env_variables['KONG_SSL_CERT'] = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
            self.env_variables['KONG_SSL_CERT_KEY'] = f"/etc/letsencrypt/live/{domain}/privkey.pem"

        path = 'config/kong.yaml'

        new_config = replace_env_vars(text=KONG_CONFIG, env=self.env_variables)

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_config)

    def configure(self):
        with open('.env', 'w+') as env_file:
            for key, value in self.env_variables.items():
                env_file.write(f"{key}={value}")
                env_file.write("\n")

    def deploy(self):
        if self.conf:
            self.configure()
        elif self.action == "up":
            up()
        elif self.action == "down":
            down()
        elif self.action == "up-prod":
            up_prod()
        else:
            print(f"Unknown command: {self.action}")
            print("Available commands: up, down")
            sys.exit(1)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    print(args)
    app = ComposeApp(
        action=args.get("action"),
        domain=args.get("domain"),
        email=args.get("email"),
        conf=args.get("conf")
    )

    app.deploy()
