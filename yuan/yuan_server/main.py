
'''
1 设置跨域访问
2 添加路由
'''
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from router.llm_lvm_api import api_router as demp_api
app = FastAPI()


# 启用 CORS
origins = ["http://10.233.202.137:3023"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 允许所有域名访问
    allow_credentials=True, # 允许携带cookies
    allow_methods=["*"], # 允许所有方法
    allow_headers=["*"], # 允许所有头
)
# 假设你的图片存放在 "static" 文件夹中

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(demp_api, prefix="/demo_api",tags=["测试用例"])
def Main():
    '''
    @Time    :   2024/08/12 15:19:49
    @功能    :   None
    '''
    uvicorn.run("main:app", host="127.0.0.1", port=8999, reload=True)
    pass

if __name__ == '__main__':
    Main()
    pass

