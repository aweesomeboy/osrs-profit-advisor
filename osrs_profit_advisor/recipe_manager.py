from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from osrs_profit_advisor.models import Recipe, RecipeInput


class RecipeManager:
    """Manage recipe storage in a JSON file."""

    def __init__(self, file_path: str | Path = "data/recipes.json") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[Recipe]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        recipes: list[Recipe] = []
        for entry in data:
            recipes.append(
                Recipe(
                    name=entry.get("name", "Unnamed recipe"),
                    inputs=[
                        RecipeInput(item_id=int(item.get("item_id", 0)), quantity=int(item.get("quantity", 0)))
                        for item in entry.get("inputs", [])
                    ],
                    output_item_id=int(entry.get("output_item_id", 0)),
                    output_quantity=int(entry.get("output_quantity", 1)),
                    craft_time_seconds=int(entry.get("craft_time_seconds", 0)),
                    required_skill=entry.get("required_skill"),
                    required_level=int(entry.get("required_level", 0)),
                    failure_chance=float(entry.get("failure_chance", 0.0)),
                    extra_costs=float(entry.get("extra_costs", 0.0)),
                    notes=str(entry.get("notes", "")),
                )
            )
        return recipes

    def save(self, recipes: list[Recipe]) -> None:
        payload = [recipe.to_dict() for recipe in recipes]
        with self.file_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def add_recipe(self, recipe: Recipe) -> list[Recipe]:
        recipes = self.load()
        recipes.append(recipe)
        self.save(recipes)
        return recipes

    def update_recipe(self, index: int, recipe: Recipe) -> list[Recipe]:
        recipes = self.load()
        if 0 <= index < len(recipes):
            recipes[index] = recipe
            self.save(recipes)
        return recipes

    def remove_recipe(self, index: int) -> list[Recipe]:
        recipes = self.load()
        if 0 <= index < len(recipes):
            del recipes[index]
            self.save(recipes)
        return recipes

    def filter_by_skill(self, skill: str | None) -> list[Recipe]:
        recipes = self.load()
        if not skill:
            return recipes
        skill_name = skill.strip().lower()
        return [recipe for recipe in recipes if (recipe.required_skill or "").lower() == skill_name]

    def search(self, query: str) -> list[Recipe]:
        if not query:
            return self.load()
        needle = query.strip().lower()
        return [recipe for recipe in self.load() if needle in recipe.name.lower()]
