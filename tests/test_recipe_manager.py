from __future__ import annotations

from osrs_profit_advisor.models import Recipe, RecipeInput
from osrs_profit_advisor.recipe_manager import RecipeManager


def test_recipe_manager_round_trip(tmp_path) -> None:
    recipes_path = tmp_path / "recipes.json"
    manager = RecipeManager(recipes_path)

    recipe = Recipe(
        name="Test recipe",
        inputs=[RecipeInput(item_id=1, quantity=2)],
        output_item_id=99,
        output_quantity=1,
        craft_time_seconds=90,
        required_skill="Smithing",
        required_level=10,
        failure_chance=0.2,
        extra_costs=5.0,
        notes="Example",
    )

    manager.add_recipe(recipe)
    loaded = manager.load()
    assert len(loaded) == 1
    assert loaded[0].name == "Test recipe"
    assert manager.filter_by_skill("Smithing")[0].required_level == 10


def test_recipe_manager_search() -> None:
    manager = RecipeManager("data/recipes.json")
    found = manager.search("cook")
    assert found
