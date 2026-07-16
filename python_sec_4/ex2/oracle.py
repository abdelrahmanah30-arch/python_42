import os
import sys
from dotenv import load_dotenv


REQUIRED_VARIABLES = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]


def check_hardcoded_secrets(config: dict[str, str | None]) -> bool:
    """Check that secret values are not written inside oracle.py."""
    try:
        with open(__file__, "r", encoding="utf-8") as source_file:
            source_code = source_file.read()
    except OSError:
        return False

    sensitive_values = [
        config.get("DATABASE_URL"),
        config.get("API_KEY"),
    ]

    for secret in sensitive_values:
        if secret and secret in source_code:
            return False

    return True


def check_production_override(env_path: str) -> bool:
    """Check that system variables have priority over .env values."""
    had_original_value = "MATRIX_MODE" in os.environ
    original_value = os.environ.get("MATRIX_MODE")

    os.environ["MATRIX_MODE"] = "production"

    load_dotenv(
        dotenv_path=env_path,
        override=False,
    )

    override_works = (
        os.getenv("MATRIX_MODE") == "production"
    )

    if had_original_value and original_value is not None:
        os.environ["MATRIX_MODE"] = original_value
    else:
        os.environ.pop("MATRIX_MODE", None)

    return override_works


def main() -> int:
    base_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    env_path = os.path.join(
        base_directory,
        ".env",
    )

    production_override_works = check_production_override(
        env_path
    )

    load_dotenv(
        dotenv_path=env_path,
        override=False,
    )

    config = {
        name: os.getenv(name)
        for name in REQUIRED_VARIABLES
    }

    missing_variables = [
        name
        for name, value in config.items()
        if not value
    ]

    matrix_mode = config.get("MATRIX_MODE")
    log_level = config.get("LOG_LEVEL")
    zion_endpoint = config.get("ZION_ENDPOINT")

    mode_is_valid = matrix_mode in (
        "development",
        "production",
    )

    zion_is_valid = bool(
        zion_endpoint
        and zion_endpoint.startswith("https://")
    )

    env_is_valid = (
        os.path.isfile(env_path)
        and not missing_variables
        and mode_is_valid
        and zion_is_valid
    )

    no_hardcoded_secrets = check_hardcoded_secrets(
        config
    )

    print("ORACLE STATUS: Reading the Matrix...\n")

    if missing_variables:
        print("\nMissing required environment variables:")

        for name in missing_variables:
            print(f"- {name}")

    print("Configuration loaded:")
    print(f"Mode: {matrix_mode or 'Unavailable'}")

    if config.get("DATABASE_URL"):
        if matrix_mode == "production":
            print(
                "Database: Connected to production instance"
            )
        else:
            print(
                "Database: Connected to local instance"
            )
    else:
        print("Database: Not connected")

    if config.get("API_KEY"):
        print("API Access: Authenticated")
    else:
        print("API Access: Not authenticated")

    print(f"Log Level: {log_level or 'Unavailable'}")

    if zion_is_valid:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")

    print("\nEnvironment security check:")

    if no_hardcoded_secrets:
        print("[OK] No hardcoded secrets detected")
    else:
        print("[KO] Hardcoded secrets detected")

    if env_is_valid:
        print("[OK] .env file properly configured")
    else:
        print(
            "[KO] .env file is not properly configured"
        )

    if production_override_works:
        print("[OK] Production overrides available")
    else:
        print(
            "[KO] Production overrides are not available"
        )

    if not env_is_valid or not no_hardcoded_secrets:
        print(
            "The Oracle cannot access all configurations."
        )
        return 1

    print("\nThe Oracle sees all configurations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
