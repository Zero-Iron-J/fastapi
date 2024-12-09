from pydantic import BaseModel

class Market(BaseModel):
    name : str
    location : str
    menu : dict[str,int]
    call_num : str