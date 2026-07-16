from pydantic import BaseModel, ValidationError
from pydantic import Field, model_validator
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not any(
            member.rank in (Rank.CAPTAIN, Rank.COMMANDER)
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            experienced_crew = sum(
                1
                for member in self.crew
                if member.years_experience >= 5
            )

            required_experienced = (len(self.crew) + 1) // 2

            if experienced_crew < required_experienced:
                raise ValueError(
                    "Long missions require at least 50% experienced crew"
                )

        if not all(member.is_active for member in self.crew):
            raise ValueError(
                "All crew members must be active"
            )

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    try:
        commander = CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=42,
            specialization="Mission Command",
            years_experience=18,
        )
        officer = CrewMember(
            member_id="CM051",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=29,
            specialization="Engineering",
            years_experience=13,
        )
        lieutenant = CrewMember(
            member_id="CM071",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=37,
            specialization="Navigation",
            years_experience=15,
        )

        crew_list = [
            commander,
            lieutenant,
            officer
        ]
        mission = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime(2025, 7, 15, 14, 12),
            duration_days=900,
            budget_millions=2500.0,
            crew=crew_list,
            mission_status="planned"
        )
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")
        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) - "
                f"{member.specialization}"
            )
    except ValidationError as error:
        message = error.errors()[0]["msg"]
        print(message.removeprefix("Value error, "))

    try:
        print("\n=========================================")
        cadet = CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.CADET,
            age=42,
            specialization="Mission Command",
            years_experience=18,
        )
        officer = CrewMember(
            member_id="CM051",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=29,
            specialization="Engineering",
            years_experience=13,
        )
        lieutenant = CrewMember(
            member_id="CM071",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=37,
            specialization="Navigation",
            years_experience=15,
        )

        crew_list = [
            cadet,
            lieutenant,
            officer
        ]
        mission = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime(2025, 7, 15, 14, 12),
            duration_days=900,
            budget_millions=2500.0,
            crew=crew_list,
            mission_status="planned"
        )
    except ValidationError as error:
        print("Expected validation error:")
        message = error.errors()[0]["msg"]
        print(message.removeprefix("Value error, "))


if __name__ == "__main__":
    main()
