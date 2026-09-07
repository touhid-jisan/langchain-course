from pydantic import BaseModel, EmailStr

class Address(BaseModel):
    country: str
    city: str
    zip: int

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address



if __name__ == "__main__":
    address = {'country':'Bangladesh', 'city': 'dhaka', 'zip': 1000}
    patient_dict = {'name': 'Ross','age':40, 'gender': 'male', 'address': Address(**address)}
    patient_1 = Patient(**patient_dict)
    print(patient_1)
