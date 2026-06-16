from fastapi import FastAPI, Path ,HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

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

