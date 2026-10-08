# Adding recipes

## Method 1: JSON file

Edit `data/recipes.json` and add or remove entries. Keep the structure consistent with the sample format in the README.

## Method 2: In-app editing

Open the Recipes tab and add a new recipe with the required fields:

- recipe name
- input items and quantities
- output item and quantity
- skill and required level
- failure chance
- extra costs
- notes

## Validation checks

- input quantities must be positive
- output quantity must be greater than zero
- skill names should match the configured filters
- invalid item IDs should be flagged during validation
