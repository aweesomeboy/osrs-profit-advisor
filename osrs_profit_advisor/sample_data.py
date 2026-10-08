from __future__ import annotations

from osrs_profit_advisor.recipe_manager import RecipeManager


def create_sample_recipe_file(path: str = "data/recipes.json") -> None:
    manager = RecipeManager(path)
    if manager.load():
        return
    manager.save([
        {
            "name": "Example recipe",
            "inputs": [{"item_id": 1, "quantity": 1}],
            "output_item_id": 2,
            "output_quantity": 1,
            "craft_time_seconds": 60,
            "required_skill": "Cooking",
            "required_level": 30,
            "failure_chance": 0.0,
            "extra_costs": 0.0,
            "notes": "Example only",
        }
    ])
