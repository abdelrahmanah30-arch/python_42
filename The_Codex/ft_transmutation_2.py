import alchemy
from elements import create_fire, create_water

print("=== Transmutation 2 ===")
print("Import alchemy module only")
print(
    "Testing lead to gold: "
    f"{alchemy.lead_to_gold()}"
    f" '{create_fire()}'"
    f" and '{create_water()}' mixed with '{create_fire()}'"
)
