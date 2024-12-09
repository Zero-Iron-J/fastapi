from pydantic import BaseModel, EmailStr

class Customer(BaseModel):
    name : str
    home : str
    call_num : str
    email : EmailStr