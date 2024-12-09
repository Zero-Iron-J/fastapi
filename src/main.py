# 필수 프레임워크를 가져온다.
from fastapi import FastAPI, Body, Header
import uvicorn

# 여기서부터 파일 import
from web import customer
from web import market
from web import user
from web import html
from web import login

# app을 실행한다.
app = FastAPI()

# 이부분에서 web에 작성된 router를 연결한다.
app.include_router(customer.router)
app.include_router(market.router)
app.include_router(user.router)
app.include_router(html.router)
app.include_router(login.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)