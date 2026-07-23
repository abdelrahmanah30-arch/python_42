import time
from functools import wraps
from typing import Callable, ParamSpec

P = ParamSpec("P")


def spell_timer(
    func: Callable[P, str],
) -> Callable[P, str]:
    @wraps(func)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> str:
        print(f"Casting {func.__name__}...")

        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        print(
            "Spell completed in "
            f"{execution_time:.3f} seconds"
        )

        return result

    return wrapper


def power_validator(
    min_power: int,
) -> Callable[
    [Callable[P, str]],
    Callable[P, str],
]:
    def decorator(
        func: Callable[P, str],
    ) -> Callable[P, str]:
        @wraps(func)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> str:
            power: object | None = kwargs.get("power")

            if power is None and args:
                power = args[-1]

            if (
                not isinstance(power, int)
                or power < min_power
            ):
                return "Insufficient power for this spell"

            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(
    max_attempts: int,
) -> Callable[
    [Callable[P, str]],
    Callable[P, str],
]:
    def decorator(
        func: Callable[P, str],
    ) -> Callable[P, str]:
        @wraps(func)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> str:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except Exception:
                    if attempt < max_attempts:
                        print(
                            "Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                        )

            return (
                "Spell casting failed after "
                f"{max_attempts} attempts"
            )

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return (
            len(name) >= 3
            and all(
                character.isalpha()
                or character.isspace()
                for character in name
            )
        )

    @power_validator(10)
    def cast_spell(
        self,
        spell_name: str,
        power: int,
    ) -> str:
        return (
            f"Successfully cast {spell_name} "
            f"with {power} power"
        )


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(3)
def unstable_spell() -> str:
    raise RuntimeError("The spell failed")


@power_validator(10)
def war_cry(power: int) -> str:
    return "Waaaaaaagh spelled !"


def main() -> None:
    print("Testing spell timer...")
    print(f"Result: {fireball()}")

    print("\nTesting retrying spell...")
    print(unstable_spell())

    print(war_cry(15))

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Gandalf"))
    print(MageGuild.validate_mage_name("Al2"))

    guild = MageGuild()

    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
