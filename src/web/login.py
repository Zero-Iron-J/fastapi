from fastapi import APIRouter, Request, Form, Response, HTTPException
from model.user import User
from service import user as service
from datetime import timedelta

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse


router = APIRouter(prefix="/login")

#기본 템플릿 위치를 지정합니다.
templates = Jinja2Templates(directory="templates")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 인증에러를 쉽게 처리하기 위해 에러함수를 작성한다.
def unauthed():
    raise HTTPException(
            status_code= 401,
            detail="올바르지 않은 인증정보입니다.",
            headers={"WWW-Authenticate" : "Bearer"}
        )

@router.get("")
@router.get("/", response_class=HTMLResponse)
def get_login_page(request : Request):
    return templates.TemplateResponse("login.html",
        {"request" : request})

# 로그인을 처리한다.
@router.post("")
@router.post("/", response_class=HTMLResponse)
def login(
    request : Request,
    response : Response,
    user_name = Form(...),
    user_password = Form(...)
):
    # 인증 -> 유저의 존재를 확인하고 + 비밀번호를 확인하는 총체
    user = service.auth_user(user_name, user_password)
    if not user:
        unauthed()

    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data = {"sub" : user.name},
        expire = expire
    )
    response = RedirectResponse("/html", status_code=302)
    response.set_cookie(key="token", value=access_token)
    return response
