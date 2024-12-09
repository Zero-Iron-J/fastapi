from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User, DB_User
from service import user as service
from datetime import timedelta
from error import Duplicate, Missing

router = APIRouter(prefix="/user")

# jtw에 사용할 기본데이터를 설정한다.
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2 = OAuth2PasswordBearer(tokenUrl="/user/token")

# 인증에러를 쉽게 처리하기 위해 에러함수를 작성한다.
def unauthed():
    raise HTTPException(
            status_code= 401,
            detail="올바르지 않은 인증정보입니다.",
            headers={"WWW-Authenticate" : "Bearer"}
        )

# OAuth2가 사용할 POST 접근을 생성해준다.
@router.post("/token")
async def create_access_token(
    form_data : OAuth2PasswordRequestForm = Depends()
):
    # username과 password를 Oauth양식에서 꺼낸뒤 JWT 토큰을 발행
    # 인증 => 유저의 존재를 확인 + 비밀번호 확인의 총체

    user = service.auth_user(form_data.username, form_data.password)

    # 유저가 있으면 사용 없으면 에러
    if not user:
        unauthed()

    # 유저가 존재한다. 인증된 사용자이다.
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data = {"sub" : user.name},
        expire = expire
    )

    return {"access_token" : access_token, "token_type" : "bearer"}


#======================
@router.post("/")
def create_user(user: DB_User):
    try :
        return service.create_user(user)
    except Duplicate as E:
        raise HTTPException(status_code=401, detail=E.msg)
    
@router.get("/user_only")
def check_user(token : str = Depends(oauth2)):
    if service.check_user(token):
        return "인증된 유저로 게시판에 접근이 가능합니다."
    raise HTTPException(status_code=401, detail="게시판에 접근권한이 없습니다. 등급을 올려주세요")
    
@router.get("/{username}")
def find_user(username):
    return service.find_user(username)