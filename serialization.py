from pydantic import BaseModel 

class Address(BaseModel):

    street:str
    city:str
    state:str
    pincode:int

class patient(BaseModel):
    name:str
    age:int
    address:Address

address_dict={'street':'123 main street', 'city':'mumbai','state':'maharashtra','pincode':400012}

address1= Address(**address_dict)

patient_dict={'name':'aayush','age':20,'address':address1}

patient1=patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.street)
print(patient1.address.city)
print(patient1.address.pincode)
print(patient1.address.state)

temp= patient1.model_dump(include=['name','age']) 
print(temp)
print(type(temp))

temp1= patient1.model_dump_json(exclude={'address':['state']}) #convert the pydantic model in a dict
print(temp1)
print(type(temp1))
