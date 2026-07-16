from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    try:
        spacestation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 7, 14, 10, 30),
            is_operational=True
        )
        print(f"ID: {spacestation.station_id}")
        print(f"Name: {spacestation.name}")
        print(f"Crew: {spacestation.crew_size} people")
        print(f"Power: {spacestation.power_level}%")
        print(f"Oxygen: {spacestation.oxygen_level}%")
        print(
            "Status: "
            f"{
                'Operational' if spacestation.is_operational
                else 'not Operational'
            }"
        )
    except ValidationError as error:
        print(error.errors()[0]["msg"])
    try:
        print("\n========================================")
        print("Expected validation error:")
        spacestation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=26,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 7, 14, 10, 30),
            is_operational=True
        )
    except ValidationError as error:
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
