from pydantic import BaseModel, EmailStr, Field, field_validator

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: list[str]
    contact_details: dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domain = ['hibc.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        return value


    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()


    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0<value<100:
            return value
        else:
            raise ValueError("Age should be between 0 and 100")
         
def get_patient_data(patient: Patient) -> None:
    print(patient)


if __name__ == "__main__":
    patient =  {"name": "Ross Geller", "email": "ross@hibc.com", "age": 30, "weight": 40.4, "married": True, "allergies": ['a', 'b'], "contact_details": {"phone": "2323232"}}
    patient1 = Patient(**patient)
    get_patient_data(patient1)