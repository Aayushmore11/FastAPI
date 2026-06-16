from pydantic import BaseModel , EmailStr , AnyUrl ,Field,  computed_field
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
    height:float

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight/self.height**2,2)
        return bmi 

patient_info={'name':'nitish','age':'40','email':'abc@hdfc.com', 'weight':70.5, 'married':True,'allergies': ['pollen'], 'contact_details': {'email': 'abc@gmail.com', 'phone': '9812345667'},'height':1.67}

patient1=Patient(**patient_info)


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.bmi)


    print('updated')

update_patient_data(patient1)


    
