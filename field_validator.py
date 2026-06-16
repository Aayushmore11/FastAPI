from pydantic import BaseModel , EmailStr , AnyUrl ,Field,  field_validator
from typing import List, Dict, Optional, Annotated

#data validation using pydantic
class Patient(BaseModel):
    
    name:str 
    age:int
    email:EmailStr
    weight:float
    married:bool
    allergies:List[str]
    contact_details:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls , value):

        valid_domains=['hdfc.com','icici.com']

        domain_name=value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Invalid email domain")
        
        return value
    
    @field_validator('name')
    @classmethod
    def transfrom_name(cls, value):
        return value.upper()      

        
def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print('inserted')

patient_info={'name':'nitish','age':30,'email':'abc@hdfc.com', 'weight':70.5, 'married':True,'allergies': ['pollen'], 'contact_details': {'email': 'abc@gmail.com', 'phone': '9812345667'}}

patient1=Patient(**patient_info)

insert_patient_data(patient1)

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)


    print('updated')

update_patient_data(patient1)


    
