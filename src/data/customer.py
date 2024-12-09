from model.customer import Customer
import sqlite3
from sqlite3 import IntegrityError
from .init import conn, curs
from error import Missing, Duplicate

curs.execute(""" create table if not exists customer(
            name text primary key,
            home text,
            call_num text,
            email text
            )
""")

# 데이터 변환에 사용될 함수들
def row_to_model(row : tuple) -> Customer:
    name, home, call_num, email = row
    return Customer(
        name = name,
        home = home,
        call_num = call_num,
        email = email
    )

def model_to_dict(customer : Customer) -> dict:
    return customer.model_dump()

# 모든 고객의 정보를 가져온다.
def get_all() -> list[Customer]:
    sql = "SELECT * FROM Customer"
    curs.execute(sql)
    datas = curs.fetchall()
    return [row_to_model(data) for data in datas]

def get_customer(customer_name)-> Customer | None:
    sql = "SELECT * FROM Customer WHERE name = :name"
    params = {"name" : customer_name}
    curs.execute(sql, params)
    data = curs.fetchone()
    if data:
        return row_to_model(data)
    else:
        raise Missing(msg=f"customer {customer_name} not found")

# 새로운 고객을 생성한다.
def create_customer(new_customer : Customer) -> Customer:
    sql = "INSERT INTO customer (name, home,call_num,email) values(:name, :home, :call_num,:email)"
    params = model_to_dict(new_customer)
    try:
        curs.execute(sql, params)
    except IntegrityError:
        raise Duplicate(msg=f"customer {new_customer.name} is already exist")
    
    conn.commit()
    return get_customer(new_customer.name)

# 기존 고객을 업데이트한다.
def modify_customer(customer_name : str, modi_customer:Customer) -> Customer:
    sql = """UPDATE customer set name=:name, home=:home,call_num=:call_num,
    email=:email WHERE name = :customer_name
    """
    params = model_to_dict(modi_customer)
    params["customer_name"] = customer_name
    curs.execute(sql, params)
    if curs.rowcount == 1:
        conn.commit()
        return get_customer(modi_customer.name)
    else:
        raise Missing(msg=f"customer {customer_name} not found")

# 고객을 삭제합니다.
def delete_customer(customer_name : str) -> None:
    sql = "DELETE FROM customer WHERE name = :name"
    params = {"name" : customer_name}
    curs.execute(sql, params)
    if curs.rowcount != 1:
        raise Missing(f"customer {customer_name} not found")
    conn.commit()
    return None