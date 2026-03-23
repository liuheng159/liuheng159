#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

MODEL_TEMPLATE = '''from dataclasses import dataclass


@dataclass
class {class_name}Payload:
    name: str
'''

SERVICE_TEMPLATE = '''from dataclasses import dataclass
from uuid import uuid4


@dataclass
class {class_name}Item:
    id: str
    name: str


class {class_name}Service:
    def __init__(self) -> None:
        self._items: dict[str, {class_name}Item] = {{}}

    def list_items(self) -> list[{class_name}Item]:
        return list(self._items.values())

    def create_item(self, name: str) -> {class_name}Item:
        item = {class_name}Item(id=str(uuid4()), name=name.strip())
        self._items[item.id] = item
        return item
'''

HANDLER_TEMPLATE = '''from app.services.{feature_name}_service import {class_name}Service

service = {class_name}Service()


def list_{feature_name}() -> list[dict]:
    return [{{"id": item.id, "name": item.name}} for item in service.list_items()]


def create_{feature_name}(payload: dict) -> dict:
    name = str(payload.get("name", "")).strip()
    if not name:
        raise ValueError("name is required")
    item = service.create_item(name)
    return {{"id": item.id, "name": item.name}}
'''

TEST_TEMPLATE = '''import unittest

from app.services.{feature_name}_service import {class_name}Service


class {class_name}ServiceTestCase(unittest.TestCase):
    def test_create_item(self) -> None:
        service = {class_name}Service()
        item = service.create_item("demo")

        self.assertEqual(item.name, "demo")
        self.assertEqual(len(service.list_items()), 1)


if __name__ == "__main__":
    unittest.main()
'''


def to_class_name(feature_name: str) -> str:
    return ''.join(part.capitalize() for part in feature_name.replace('-', '_').split('_'))


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a backend feature skeleton.")
    parser.add_argument("feature_name")
    parser.add_argument("--app-dir", default="app")
    parser.add_argument("--tests-dir", default="tests")
    args = parser.parse_args()

    feature_name = args.feature_name.replace('-', '_')
    class_name = to_class_name(feature_name)
    app_dir = Path(args.app_dir)
    tests_dir = Path(args.tests_dir)

    write_file(
        app_dir / "models" / f"{feature_name}.py",
        MODEL_TEMPLATE.format(class_name=class_name),
    )
    write_file(
        app_dir / "services" / f"{feature_name}_service.py",
        SERVICE_TEMPLATE.format(class_name=class_name),
    )
    write_file(
        app_dir / "handlers" / f"{feature_name}.py",
        HANDLER_TEMPLATE.format(class_name=class_name, feature_name=feature_name),
    )
    write_file(
        tests_dir / f"test_{feature_name}_service.py",
        TEST_TEMPLATE.format(class_name=class_name, feature_name=feature_name),
    )

    print(f"Created backend feature skeleton for '{feature_name}'.")


if __name__ == "__main__":
    main()
