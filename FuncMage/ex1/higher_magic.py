from typing import Callable


def fireball_for_test(target: str, power: int) -> str:
    return f"Fireball hits {target} and power {power}"


def heal_for_test(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def spell_combiner(
    spell1: Callable[[str, int], str],
    spell2: Callable[[str, int], str],
) -> Callable[[str, int], tuple[str, str]]:
    def spell(
        target: str,
        power: int,
    ) -> tuple[str, str]:
        result1 = spell1(target, power)
        result2 = spell2(target, power)

        return result1, result2

    return spell


def power_amplifier(
        base_spell: Callable[[str, int], str],
        multiplier: int,
) -> Callable[[str, int], str]:
    def spell(target: str, power: int) -> str:
        amplified_power = power * multiplier
        result = base_spell(target, amplified_power)
        return result

    return spell


def conditional_caster(
        condition: Callable[[str, int], bool],
        spell: Callable[[str, int], str]
) -> Callable[[str, int], str]:
    def condition_spell(target: str, power: int) -> str:
        if not condition(target, power):
            return "Spell fizzled"

        result = spell(target, power)
        return result

    return condition_spell


def spell_sequence(
        spells: list[Callable[[str, int], str]]
) -> Callable[[str, int], list[str]]:
    def sequence_spell(
            target: str,
            power: int
    ) -> list[str]:
        result: list[str] = []
        for spell in spells:
            result_spell = spell(target, power)
            result.append(result_spell)

        return result
    return sequence_spell


def enough_power(target: str, power: int) -> bool:
    return power >= 20


def power_for_test(target: str, power: int) -> str:
    return f"{power}"


def main_test() -> None:
    print("### test for combiner ###")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 10)
    i = 0
    for item in result:
        if i != len(result) - 1:
            print(item, end=", ")
            i += 1
        else:
            print(item)
    print("\n### test for amplifier ###")
    mega_heal = power_amplifier(heal_for_test, 3)

    print(heal_for_test("Dragon", 10))
    print(mega_heal("Dragon", 10))

    print("\n### test for condition caster ###")
    conditional_fireball = conditional_caster(
        enough_power,
        fireball_for_test,
    )
    print(conditional_fireball("dragon", 10))
    print(conditional_fireball("dragon", 30))
    print("\n### test for spell sequence ###")
    spells: list[Callable[[str, int], str]] = [
            fireball_for_test,
            heal_for_test,
            fireball,
            heal,
        ]
    sequence = spell_sequence(
        spells
    )
    for item in sequence("dragon", 10):
        print(item)


def main() -> None:
    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 10)
    i = 0
    print("Combined spell result: ", end="")
    for item in result:
        if i != len(result) - 1:
            print(item, end=", ")
            i += 1
        else:
            print(item)

    print("\nTesting power amplifier...")
    original_spell = 10
    amplifier = power_amplifier(power_for_test, 3)
    print(
        f"Original: {original_spell}, "
        f"Amplified: {amplifier('dragon', original_spell)}\n"
    )


if __name__ == "__main__":
    main()
