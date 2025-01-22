from pydantic import BaseModel
from fastapi import APIRouter, Request
api_router = APIRouter()

def ReadAndWriteJson(json_file, datas={}, model=0):
    '''
    @Time    :   2024/05/22 13:43:44
    @功能    :   读/写json文件
        model: 
            0:读取数据；1:追加写入数据；2:修改数据；3:覆写数据
       datas 结构{"a":{"aa":"bb"}}
    '''
    import json
    # 读取JSON文件
    def read_json():
        try:
            with open(json_file, 'r', encoding="utf-8") as file:
                data = json.load(file)
        except: data = {}
        return data
    # 写入JSON文件
    def write_json(json_data):
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False,indent=4)
    if model == 0:
        # 读取json数据
        return read_json()
    elif model == 1:
        # 追加写入json数据
        old_datas = read_json()
        write_json(old_datas+datas)
        return old_datas+datas
    elif model == 2:
        # 修改json数据; 返回原数据
        old_datas = read_json()
        write_json(datas)
        return old_datas
    elif model == 3:
        # 覆写json数据
        old_datas = read_json()
        write_json(datas)
        return old_datas
    else:
        print("操作excel的模式不对。请对照修改 0:读取数据；1:追加写入数据；2:修改数据；3:覆写数据(清空数据，重新写入)")
        return None
datas_json = ReadAndWriteJson("../datas.json")

class Item(BaseModel):
    """
    Pydantic model, 自动根据数据生成字段
    """
    id:str
    llm_model:str
    cl:str
    arn:str
    feature:str
    soc:str
    token_rates:str

@api_router.get('/search/{id}',
        summary='查询',
        description='根据字段和输入内容做模糊查询',
        response_description='响应的描述信息')
async def search(request:Request):
    return {}

@api_router.delete('/del/{id}',
        summary='根据id删除数据',
        description='详细描述',
        response_description='响应的描述信息')
async def Del(request:Request):
    return {}

@api_router.post('/add',
        summary='新增数据',
        description='详细描述',
        response_description='响应的描述信息')
async def Add(request:Request):
    return {}

@api_router.update('/update',
        summary='更新数据',
        description='详细描述',
        response_description='响应的描述信息')
async def update(request:Request):
    return {}

@api_router.get('/sort',
        summary='排序数据',
        description='详细描述',
        response_description='响应的描述信息')
async def sort(request:Request):
    return {}


@api_router.get('/details',
        summary='笔记详情',
        description='详细描述',
        response_description='响应的描述信息')
async def details(request:Request):
    context = {
        "request":request,
        'name': 'John Doe',
        'username': 'johndoe', 
        'email': 'johndoe@example.com',
        'avatar_url': 'path/to/avatar.jpg',
    }

    return {}

@api_router.get('/detail/{id}',
        summary='笔记详情',
        description='详细描述',
        response_description='响应的描述信息')
async def detail(request:Request, id:int):
    context = {
        "request":request,
        'name': 'John Doe',
        'username': 'johndoe', 
        'email': 'johndoe@example.com',
        'avatar_url': 'path/to/avatar.jpg',
    }

    return {}
