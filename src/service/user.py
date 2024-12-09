from datetime import timedelta, datetime
from jose import jwt
import bcrypt
from data import user as data
from model.user import User, DB_User
from fastapi import HTTPException

# 시크릿 키를 설정
SECRET_KEY = "11B0BF668EBCA3E6F00DFD8954AA21533B022E879DF385FD38C5174A6E6EB727"
ALGORITHM = "HS256"

# ========= 지원을 위한 기능들 ================
# 유저를 찾는기능
def find_user(username):
    if (user := data.find_user(username) ):
        return user
    return None

# 비밀번호를 확인하는 기능
def verify_password(password : str, hashed_password :str):
    password = password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")
    is_valid = bcrypt.checkpw(password, hashed_password)
    return is_valid

# 비밀번호를 해시하는 기능
def make_hash_password(password : str):
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password.decode("utf-8")


# post token
def auth_user(username, password):
    # 유저를 확인한다.
    user = find_user(username)
    if not user:
        return None
    password_check = verify_password(password, user.hashed_password)
    if not password_check:
        return None
    return user

def create_access_token(data : dict, expire : timedelta):
    data = data.copy()
    now = datetime.utcnow()
    data.update({"exp" : now + expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#++++++++++++CRUD++++++++++++++++
def create_user(user: DB_User):
    user = DB_User(name=user.name, email=user.email, hashed_password= make_hash_password(user.hashed_password))
    return data.create_user(user)


# =================================

# 토큰을 분해한다.
def decode_token(token:str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    if not (username := payload.get("sub")):
        return None
    return username

# 유저를 가져온다
def get_current_user(token:str):
    # 토큰을 분해하는 친구에게 토큰분해를 요청
    username = decode_token(token)
    # 분해가된 데이터를 이용하여 유저 정보를 가져온다.
    user = find_user(username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="올바르지 않은 인증정보입니다.",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    return user.name


# 가짜 데이터를 만든다.
_fake_db = {"spongebob" : True, "jane" : False}

# web에서 요청한 checkuser를 반환한다.
# 게시판에 접근 가능한지 여부를 판단한다.
def check_usable(token:str):
    username = get_current_user(token)
    # 인가 데이터베이스를 조회하여 접근여부를 결정
    if _fake_db[username]:
        return True
    return False

def check_user(token :str):
    check = check_usable(token)
    return check