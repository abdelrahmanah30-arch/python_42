from typing import TypedDict


class Artifact(TypedDict):
    name: str
    power: int
    type: str


class Mage(TypedDict):
    name: str
    power: int
    element: str


class MageStats(TypedDict):
    max_power: int
    min_power: int
    avg_power: float


def artifact_sorter(
    artifacts: list[Artifact]
) -> list[Artifact]:
    sorted_artifacts = sorted(
        artifacts,
        key=lambda artifact: artifact["power"],
        reverse=True
    )

    return sorted_artifacts


def power_filter(
    mages: list[Mage], min_power: int
) -> list[Mage]:
    filters = list(
        filter(
            lambda mage: mage["power"] >= min_power,
            mages
        )
    )
    return filters


def spell_transformer(spells: list[str]) -> list[str]:
    trans = list(
        map(
            lambda spells: "* " + spells + " *",
            spells
        )
    )

    return trans


def mage_stats(
    mages: list[Mage]
) -> MageStats:
    max_power = max(
        mages,
        key=lambda mages: mages["power"]
    )["power"]

    min_power = min(
        mages,
        key=lambda mages: mages["power"]
    )["power"]

    avg_power = 0.0
    avg_power = round(
        sum(map(lambda mage: mage["power"], mages)) / len(mages),
        2
    )
    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power
    }


def main() -> None:
    artifacts: list[Artifact] = [
        {"name": "Crystal Orb", "power": 85, "type": "orb"},
        {"name": "Fire Staff", "power": 92, "type": "staff"}
    ]
    sorted_artifacts = artifact_sorter(artifacts)
    print("Testing artifact sorter...")
    print(
        f"{sorted_artifacts[0]["name"]}"
        f" ({sorted_artifacts[0]["power"]} power)"
        " comes befor "
        f"{sorted_artifacts[1]["name"]} "
        f"({sorted_artifacts[1]["power"]} power)\n"
    )
    print("Testing spell transformer...")
    spells = ["Fireball", "Heal", "Shield"]
    spell = spell_transformer(spells)
    for item in spell:
        print(item, end=" ")
    print()


if __name__ == "__main__":
    main()
