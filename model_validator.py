from pydantic import BaseModel , EmailStr , AnyUrl ,Field,  model_validator
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

    @model_validator(mode='after')
    def vaidate_emergency_contact(cls,model):
        if model.age>65 and "emergency" not in model.contact_details:
            raise ValueError("emergency contact is required for patients above 60 ")
        return model

patient_info={'name':'nitish','age':'40','email':'abc@hdfc.com', 'weight':70.5, 'married':True,'allergies': ['pollen'], 'contact_details': {'email': 'abc@gmail.com', 'phone': '9812345667'}}

patient1=Patient(**patient_info)


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


    
