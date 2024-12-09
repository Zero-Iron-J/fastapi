import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic = HTTPBasic()

secret_user : str = "agent001"
secret_password : str = "its001"

@app.get("/check")
def get_user(creds : HTTPBasicCredentials = Depends(basic)):
    if (creds.username == secret_user and creds.password == secret_password):
        return "wellcom its home"
    else:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")

if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)