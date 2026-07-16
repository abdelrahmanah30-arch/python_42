from pydantic import ValidationError, model_validator
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError(
                "Physical contact reports must be verified"
            )
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if (
            self.signal_strength > 7.0
            and (
                self.message_received is None
                or not self.message_received.strip()
            )
        ):
            raise ValueError(
                "Strong signals should include received messages"
            )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    try:
        aliencontact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2026, 7, 14, 10, 30),
            contact_type=ContactType.RADIO,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            is_verified=False,
            message_received="’Greetings from Zeta Reticuli’"
        )
        print(f"ID: {aliencontact.contact_id}")
        print(f"Type: {aliencontact.contact_type.value}")
        print(f"Location: {aliencontact.location}")
        print(f"Signal: {aliencontact.signal_strength}/10")
        print(f"Duration: {aliencontact.duration_minutes} minutes")
        print(f"Witnesses: {aliencontact.witness_count}")
        print(f"Message: {aliencontact.message_received}")
    except ValidationError as error:
        print(error.errors()[0]["msg"])
    try:
        print("\n======================================")
        print("Expected validation error:")
        aliencontact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2026, 7, 14, 10, 30),
            contact_type=ContactType.TELEPATHIC,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            is_verified=False,
            message_received="’Greetings from Zeta Reticuli’"
        )
        print(aliencontact.witness_count)
    except ValidationError as error:
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
