import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

# 사용할 데이터의 형태를 구현
class User(BaseModel):
    name : str
    email : str

class DB_User(User):
    hashed_password : str

# 가상의 데이터베이스를 구현
fake_user_db = {
    "spongebob" : {
        "name" : "spongebob",
        "email" : "sponge@gmail.com",
        "hashed_password" : "hashed_1234",
        "active" : False
    },
    "jane" : {
        "name" : "jane",
        "email" : "jane123@naver.com",
        "hashed_password" : "hashed_6789",
        "active" : True
    }
}

# 로그인을 지원하기 위해 필요한 함수들
def fake_hash_password(password : str):
    return "hashed_" + password

# 로그인 기능을 구현

@app.post("/token")
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    # 데이터베이스에서 유저를 검색한다. (이미 가입된 유저여야한다.)
    user_dict = fake_user_db.get(form_data.username)

    # 유저가 있으면 유저를 사용하면되고 없으면? 에러를 발생시킨다.
    if not user_dict:
        raise HTTPException(status_code=400, detail="아이디와 비밀번호를 정확하게 입력해주세요")
        
    # 유저이름 즉 id는 맞는 상태에서 password를 확인한다.
    h_password = fake_hash_password(form_data.password)

    # 해시된 비밀번호와 데이터베이스에 저장된 비밀번호가 다르다면?
    if not h_password == user_dict["hashed_password"]:
        raise HTTPException(status_code=400, detail="아이디와 비밀번호를 정확하게 입력해주세요")
    
    # 현상태는 유저도 존재하고 비밀번호도 올바르게 입력한 상태
    return {"access_token" : user_dict["name"], "token_type" : "bearer"}

#====================================================

# 유저데이터를 가져오는 친구
def get_user(db, username : str):
    user_dict = db[username]
    return user_dict

# 토큰을 해체하여 유저를 가져오는 함수
def fake_decode_token(token : str):
    user = get_user(fake_user_db, token)
    return user

# 토큰을 넘겨준 유저의 정보를 가져온다.
async def get_current_user(token:str = Depends(oauth2)):
    # 토큰을 분해하는 기능에게 분해를 요청한다.
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code= 401,
            detail="올바르지 않은 인증정보입니다.",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    return user


# 활성화된 유저인가?
async def get_current_active_user(current_user : dict = Depends(get_current_user)):
    if current_user["active"]:
        return current_user
    else:
        raise HTTPException(status_code=400, detail="휴면유저입니다.")

# 접속한 유저의 정보를 가져온다.
@app.get("/users/login_data")
async def read_me(current_user : dict = Depends(get_current_active_user)):
    return current_user





if __name__ == "__main__":
    uvicorn.run("oauth:app", reload=True)