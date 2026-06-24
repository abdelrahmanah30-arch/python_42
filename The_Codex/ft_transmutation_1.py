import alchemy.transmutation
from elements import create_fire, create_water

print("=== Transmutation 1 ===")
print("Import transmutation module directly")

print(
    "Testing lead to gold: "
    f"{alchemy.transmutation.recipes.lead_to_gold()}"
    f" '{create_fire()}'"
    f" and '{create_water()}' mixed with '{create_fire()}'"
)
