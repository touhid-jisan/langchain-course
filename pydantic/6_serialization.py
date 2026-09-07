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
    temp_1 = patient_1.model_dump() # dict
    temp_2 = patient_1.model_dump_json(exclude=[{'address': ['state']}, 'name'])
    temp_3 = patient_1.model_dump(include=['name', 'address'])
    print(temp_1, type(temp_1)) 
    print(temp_2, type(temp_2)) 
    print(temp_3, type(temp_3)) # dict
