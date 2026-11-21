"""Creational - Singleton: configuration manager.

Statement: https://courses.dallard.tech/sys_design/creational_pattern/
Run: python3 singleton_config.py   (reads config.json next to this file)
"""
from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).with_name("config.json")


class ConfigManager:
    _instance: ConfigManager | None = None
    _lock = threading.Lock()          # safe if two threads ask at the same time

    def __init__(self, path: Path = CONFIG_PATH) -> None:
        if ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.get_instance()")
        print(f"(loading {path.name} from disk)")
        with open(path, encoding="utf-8") as f:
            self._config: dict = json.load(f)

    @classmethod
    def get_instance(cls) -> ConfigManager:
        """Load the file on first access, then always return the same object."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def get(self, key: str, default: Any = None) -> Any:
        """Dotted access to nested values: get("database.host")."""
        value: Any = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key: str, value: Any) -> None:
        """Change a value; every module sees it, since they share the instance."""
        *parents, last = key.split(".")
        node = self._config
        for part in parents:
            node = node.setdefault(part, {})
        node[last] = value

    @classmethod
    def reset(cls) -> None:
        """Test helper: forget the instance so a test can load a fake config."""
        cls._instance = None


# --- the four "modules", now using the singleton ---------------------------
def connect_database() -> None:
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to: str, subject: str) -> None:
    config = ConfigManager.get_instance()
    print(f"Sending email from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount: float) -> None:
    config = ConfigManager.get_instance()
    print(f"Processing {amount}€ in {config.get('payment.environment')} mode")


def start_application() -> None:
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


if __name__ == "__main__":
    start_application()          # file read here, once
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)

    a, b = ConfigManager.get_instance(), ConfigManager.get_instance()
    print("same instance:", a is b)

    a.set("payment.environment", "production")
    process_payment(10.0)        # the change is visible everywhere
