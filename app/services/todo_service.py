from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List
from uuid import uuid4


@dataclass
class TodoItem:
    id: str
    title: str
    done: bool = False


class TodoService:
    def __init__(self) -> None:
        self._items: Dict[str, TodoItem] = {}

    def list_items(self) -> List[TodoItem]:
        return list(self._items.values())

    def create_item(self, title: str) -> TodoItem:
        item = TodoItem(id=str(uuid4()), title=title.strip(), done=False)
        self._items[item.id] = item
        return item

    def mark_done(self, item_id: str) -> TodoItem:
        item = self._items[item_id]
        item.done = True
        return item

    def delete_item(self, item_id: str) -> None:
        self._items.pop(item_id)

    def export_summary(self) -> List[dict]:
        return [asdict(item) for item in self.list_items()]
