from alchemy.transmutation.recipes import lead_to_gold
from elements import create_fire, create_water


print("=== Transmutation 0 ===")
print("Using file alchemy/transmutation/recipes.py directly")
print(
    f"Testing lead to gold: {lead_to_gold()} '{create_fire()}'"
    f" and '{create_water()}' mixed with '{create_fire()}'"
)
