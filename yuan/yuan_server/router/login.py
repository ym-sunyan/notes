from pydantic import BaseModel
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
app = APIRouter()

# 加载模板 当前项目之下的templates文件夹
templates = Jinja2Templates(directory=r"template\template")
# 加载模板 当前项目之下的templates文件夹

import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

# 假设的用户数据库
fake_users_db = {
    "admin": {"username": "admin", "password": "zzz"},
    "user2": {"username": "user2", "password": "000"}
}

# JWT 密钥
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 用户登录模型
class UserCredentials(BaseModel):
    username: str
    password: str

# 用户模型
class User(BaseModel):
    username: str

# 创建 JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证 JWT 的依赖项
def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token/login"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return username


@app.get('/login_page',
        summary='加载登录界面',
        description='详细描述',
        response_description='响应的描述信息')
async def login(request:Request):
    context = {
            "request":request,
        }
    return templates.TemplateResponse(
        "login.html",
        context
    )

@app.post('/login',
        summary='登录或者注册的账号信息',
        description='详细描述',
        response_description='响应的描述信息')
async def login_datas(request:Request):
    context = {
            "request":request,
        }
    return templates.TemplateResponse(
        "login.html",
        context
    )

# 用户登录端点
@app.post("/token/login")
async def login(user_credentials: UserCredentials):
    user = fake_users_db.get(user_credentials.username)
    if not user or user["password"] != user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user_credentials.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 受保护的路由
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
