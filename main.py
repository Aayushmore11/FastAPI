from fastapi import FastAPI, Path ,HTTPException, Query  
from fastapi.responses import JSONResponse
from pydantic import BaseModel  , Field , computed_field
from typing import Annotated , Literal , Optional 
import json 

app = FastAPI()

class Patient(BaseModel):   #mention all classes in the json file 
     
    id:Annotated[str,Field(...,description='Id of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='city where the patient is living')]
    age:Annotated[int,Field(...,gt=0, lt=120, description='age pf the patient')]
    gender:Annotated[Literal['male','female','others'], Field(...,description='gender of the patient')]
    height:Annotated[float, Field(...,gt=0,description='height of the patient in mtrs')]
    weight:Annotated[float,Field(...,gt=0 ,lt=150,description='weight of the patient in kgs ')]
    
    @computed_field
    @property 
    def bmi(self)-> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:   #verdict is taking heklp from bmi which is itself a omputed field A computed field is a value that is:not stored directly,calculated dynamically from other fields in the model

        if self.bmi<18.5:
            return 'underweight'
        elif self.bmi<25:
            return 'normal'
        elif self.bmi<30:
            return 'overweight'
        else:
            return 'obese'
        
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default='None')] 
    city:Annotated[Optional[str],Field(default='None')]
    age:Annotated[Optional[int],Field(default='None' , gt=0)]
    gender:Annotated[Optional[Literal['male','female']], Field(default='None')]
    height:Annotated[Optional[float], Field(default=None , gt=0)]
    weight:Annotated[Optional[float], Field(default='None' , gt=0 )]

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('patients.json', 'w')as file:
        json.dump(data,file)
    


    
    """when pydantic creates the verdict it creates or triggers this code
    which itself has a computed field in it and so 
    there it goes to the
      computed fiekd of bmi and tae infomation from there and puts to value here to check on this computed field to check its value
    basicallly one field is dependent on the other field 
    """












@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A Fully Functional Patient Management System API built with FastAPI."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description = 'ID of the Patient in the DB', example = 'P001')):
# load all the data first.  the three dots in path means that the parameter is required used to add description and example to the parameter in the docs.
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found.")

@app.get('/sort')
def sort_patients(sort_by: str= Query(..., description = ' sort the patients by height, weight,bmi '), 
order: str=Query('asc', description = 'order of sorting, asc or dsc',)):

    valid_fields=['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid field Select From:{valid_fields} ")
    if order not in ['asc','dsc']:
        raise HTTPException(status_code=400, detail="invalid order,select from:asc or dsc")
        
    data = load_data()
    sort_order= True if order=='dsc' else False
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by],reverse=(order=='dsc'))
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient): #patient here is pydantic object
    
     #:patient data is coming which is coming in request model we are sending it to the pydantic model and the pydantic model will just check if it is in a righ tformat or not 
    '''if the data is in the right format then only we lll move forwad or else we will face some error 
    we dont create or send the reqyest manuaally to the pydantic modelbehind the scenes fastapi is doing ll this work
     '''
     
     #load existing data
    data=load_data()   #the existing dataa is python dict and the patient is pydantic objject


     # check if the patients already exists 
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exists')
    

     # if patients is not there rthen we willl
     # add new patient totthe datasbase 
    data[patient.id] = patient.model_dump(exclude=['id'])
     
#save into the  json file 
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str,patient_update: PatientUpdate): 

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient Not Found')
    existing_patient_info=data[patient_id]

    updated_patient_info= patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key]= value
         
    
    #existing_patient_info -> pydantic object ->updated bmi+verdict
    existing_patient_info['id']=patient_id
    patient_pydantic_object=Patient(**existing_patient_info) 

#pydantic object -> dict
    existing_patient_info =patient_pydantic_object.model_dump(exclude='id')

#add this dict to data
    data[patient_id]=existing_patient_info

    #save data
    save_data(data) 

    return JSONResponse(status_code=200,content='patient updated')

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):

    #load data
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted'})

