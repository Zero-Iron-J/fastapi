from model.user import User, DB_User
from .init import conn, curs, IntegrityError
from error import Missing, Duplicate

# 데이터베이스 초기화
curs.execute("""
create table if not exists user(name text primary key,
            email text, hashed_password text)
""")

# 사용할 데이터의 형변환을 위한 함수들
def row_to_model(row : tuple) -> DB_User:
    name, email, hashed_password = row
    return DB_User(
        name = name,
        email = email,
        hashed_password=hashed_password
    )

def model_to_dict(user : User | DB_User):
    return user.model_dump()

# 데이터베이스에서 유저 정보를 조회한다.
def find_user(username):
    sql = "select * from user where name = :name"
    params = {"name" : username}
    curs.execute(sql, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    return row


# 데이터베이스에 유저 정보를 생성한다.
def create_user(user:DB_User):
    sql = "insert into user (name, email, hashed_password) values (:name, :email, :hashed_password)"
    params = model_to_dict(user)
    try:
        curs.execute(sql, params)
    except IntegrityError:
        raise Duplicate(msg = "이미 회원가입이 되어있습니다. 로그인으로 접근해주세요")
    conn.commit()
    return None