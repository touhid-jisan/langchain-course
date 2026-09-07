
from email.policy import default
from pydantic import BaseModel, AnyUrl, EmailStr, Field, NameEmail
from typing import Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name of the patient", description="Give the name of the patient in less than 50 chars", examples=["Ross", "Joey"])]
    email: EmailStr
    name_email: NameEmail
    linkedin: AnyUrl
    age: int
    height: float = Field(gt=0, lt=200)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=False, description="Is the patient married or not!")]
    allergies: Annotated[Optional[list[str]], Field(default=None, max_length=5)]
    contact_details: dict[str, str]


def get_patient_data(patient: Patient) -> None:
    print(patient)

if __name__ == "__main__":
    patient =  {"name": "John ABC", "age": 30, "linkedin": "https://www.linkedin.com/in/john","email":"john@example.com", "name_email": " Jhon ABC <john@example.com>", "weight": 70.5, "height": 175.0,"contact_details": {"email": "john@example.com", "phone": "1234567890"}, "allergies": ["penicillin", "latex"]}
    patient1 = Patient(**patient)
    get_patient_data(patient1)