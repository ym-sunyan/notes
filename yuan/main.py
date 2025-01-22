
# uvicorn fastapi_test:app --host 10.233.202.137 --port 7767
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi_test import app as app_router

# 启用 CORS
origins = ["http://localhost:5173"]
# 创建 FastAPI 应用实例
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 允许所有域名访问
    allow_credentials=True, # 允许携带cookies
    allow_methods=["*"], # 允许所有方法
    allow_headers=["*"], # 允许所有头
)


app.include_router(app_router, prefix="/information",tags=["个人信息"])

def Main():
    '''
    @Time    :   2024/08/12 15:19:49
    @功能    :   None
    '''
    uvicorn.run("main:app", host="10.233.202.137", port=7767, reload=True)
    pass

if __name__ == '__main__':
    Main()
    pass