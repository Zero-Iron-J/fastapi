from fastapi import APIRouter, HTTPException
from model.customer import Customer
import service.customer as service
from error import Missing, Duplicate

router = APIRouter(prefix="/customer")

@router.get("")
@router.get("/")
def get_all() -> list[Customer]:
    return service.get_all()


# 고객에 이름을 잘못적었다.
# => 조회가 되지 않는다. => None
@router.get("/{customer_name}")
def get_customer(customer_name) -> Customer | None:
    try:
        return service.get_customer(customer_name)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)

@router.post("/")
def create_customer(new_customer : Customer) -> Customer:
    try:
        return service.create_customer(new_customer)
    except Duplicate as E:
        raise HTTPException(status_code=404, detail=E.msg)

@router.put("/{customer_name}")
def modify_customer(customer_name : str, modi_customer:Customer) -> Customer:
    try:
        return service.modify_customer(customer_name, modi_customer)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)

@router.delete("/{customer_name}")
def delete_customer(customer_name : str) -> None:
    try:
        return service.delete_customer(customer_name)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)