from pydantic import BaseModel

# 사용할 데이터의 형태를 구현
class User(BaseModel):
    name : str
    email : str

class DB_User(User):
    hashed_password : str