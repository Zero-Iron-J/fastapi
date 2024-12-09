from fastapi import APIRouter, Request, Form, HTTPException
from model.customer import Customer
from service import customer as service
from service import user as user
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse


router = APIRouter(prefix="/html")

#기본 템플릿 위치를 지정합니다.
templates = Jinja2Templates(directory="templates")

# 인증에러를 쉽게 처리하기 위해 에러함수를 작성한다.
def unauthed():
    raise HTTPException(
            status_code= 401,
            detail="올바르지 않은 인증정보입니다.",
            headers={"WWW-Authenticate" : "Bearer"}
        )



@router.get("")
@router.get("/", response_class=HTMLResponse)
def get_all(request : Request):

    # 클라이언트가 보낸 토큰을 가져온다.
    token = request.cookies["token"]

    # 토큰 유효성 검사
    if user.get_current_user(token):
        customers = service.get_all()
        return templates.TemplateResponse("index.html",
            {"request" : request, "customers" : customers})
    else:
        unauthed()

# 고객 데이터를 생성한다.
@router.post("/", response_class=HTMLResponse)
def create(
    request : Request,
    name = Form(...),
    home = Form(...),
    call_num = Form(...),
    email = Form(...)
):
    # 클라이언트가 보낸 토큰을 가져온다.
    token = request.cookies["token"]

    if user.get_current_user(token):
        service.create_customer(Customer(
            name = name,
            home=home,
            call_num=call_num,
            email=email
        ))
        return RedirectResponse("/html", status_code=302)
    else:
        unauthed()


@router.post("/update", response_class=HTMLResponse)
def modify_customer(
    request : Request,
    origin_name = Form(...),
    name = Form(...),
    home = Form(...),
    call_num = Form(...),
    email = Form(...)
):
    # 클라이언트가 보낸 토큰을 가져온다.
    token = request.cookies["token"]

    if user.get_current_user(token):
        service.modify_customer(origin_name, Customer(
            name = name,
            home=home,
            call_num=call_num,
            email=email
        ))
        return RedirectResponse("/html", status_code=302)
    else:
        unauthed()



@router.post("/delete", response_class=HTMLResponse)
def delete_customer(
    request : Request,
    name = Form(...)):
    # 클라이언트가 보낸 토큰을 가져온다.
    token = request.cookies["token"]

    if user.get_current_user(token):
        service.delete_customer(name)
        return RedirectResponse("/html", status_code=302)
    else:
        unauthed()
