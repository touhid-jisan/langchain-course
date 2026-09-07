from pydantic import BaseModel, EmailStr, Field, model_validator


class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: list[str]
    contact_details: dict[str, str]

    @model_validator(mode="after")
    def validate_emergency_contact(self):
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError(
                f"Patient older than 60 must have emergency contact number"
            )
        return self


def get_patient_data(patient: Patient) -> None:
    print(patient)


if __name__ == "__main__":
    patient = {
        "name": "Ross Geller",
        "email": "ross@hibc.com",
        "age": "63",
        "weight": 62.4,
        "married": True,
        "allergies": ["a", "b"],
        "contact_details": {"phone": "2323232"},
    }
    patient1 = Patient(**patient)
    get_patient_data(patient1)
