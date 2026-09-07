from pydantic import BaseModel, EmailStr, computed_field


class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    height: float
    married: bool
    allergies: list[str]
    contact_details: dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi


def get_patient_data(patient: Patient) -> None:
    print(patient.name)
    print(patient.bmi)


if __name__ == "__main__":
    patient = {
        "name": "Ross Geller",
        "email": "ross@hibc.com",
        "age": "44",
        "weight": 62.4, # kg
        "height": 1.72, # mtr
        "married": True,
        "allergies": ["a", "b"],
        "contact_details": {"phone": "2323232"},
    }
    patient1 = Patient(**patient)
    get_patient_data(patient1)
