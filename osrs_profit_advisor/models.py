from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ItemSnapshot:
    item_id: int
    name: str
    high_price: float | None = None
    low_price: float | None = None
    avg_price: float | None = None
    volume: int | None = None
    buy_limit: int | None = None
    last_updated: str | None = None
    is_stale: bool = False


@dataclass
class RecipeInput:
    item_id: int
    quantity: int


@dataclass
class Recipe:
    name: str
    inputs: list[RecipeInput] = field(default_factory=list)
    output_item_id: int = 0
    output_quantity: int = 1
    craft_time_seconds: int = 0
    required_skill: str | None = None
    required_level: int = 0
    failure_chance: float = 0.0
    extra_costs: float = 0.0
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "inputs": [
                {"item_id": item.item_id, "quantity": item.quantity}
                for item in self.inputs
            ],
            "output_item_id": self.output_item_id,
            "output_quantity": self.output_quantity,
            "craft_time_seconds": self.craft_time_seconds,
            "required_skill": self.required_skill,
            "required_level": self.required_level,
            "failure_chance": self.failure_chance,
            "extra_costs": self.extra_costs,
            "notes": self.notes,
        }
