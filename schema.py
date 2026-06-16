
#type validation using pydantic

from pydantic import BaseModel , EmailStr , AnyUrl , Field 

from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    
    name:str 
    age:int=Field(gt=0,lt=120) 
    email:EmailStr #data validation for email using pydantic
    website:Optional[AnyUrl]=None #optional field for website, data validation for url using pydantic
    weight:Annotated[float, Field(gt=0, strict=True)] #field for weight, data validation for float using pydantic
    married:bool
    allergies:Annotated[Optional[List[str]], Field(max_length=5, default=None)]
    contact_details:Dict[str,str]

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print('inserted')

patient_info={'name':'nitish','age':30,'email':'abc@gmail.com', 'weight':70.5, 'married':True, 'contact_details': {'email': 'abc@gmail.com', 'phone': '9812345667'}}

patient1=Patient(**patient_info)

insert_patient_data(patient1)

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.website)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)


    print('updated')

update_patient_data(patient1)


#data validation using pydantic
    