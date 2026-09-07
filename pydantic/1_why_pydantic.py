
from pydantic import BaseModel, AnyUrl, EmailStr, Field, NameEmail
from typing import Optional

class Patient(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    name_email: NameEmail
    linkedin: AnyUrl
    age: int
    height: float = Field(gt=0, lt=200)
    weight: Optional[float] # must be provided but value can be None
    married: bool = False # default value False if not provided
    allergies: Optional[list[str]] = None # the field an be omitted completely
    contact_details: dict[str, str]


def get_patient_data(patient: Patient) -> None:
    print(patient)

if __name__ == "__main__":
    patient =  {"name": "John ABC", "age": 30, "linkedin": "https://www.linkedin.com/in/john","email":"john@example.com", "name_email": " Jhon ABC <john@example.com>", "weight": 70.5, "height": 175.0,"contact_details": {"email": "john@example.com", "phone": "1234567890"}, "married": True, "allergies": ["penicillin", "latex"]}
    patient1 = Patient(**patient)
    get_patient_data(patient1)