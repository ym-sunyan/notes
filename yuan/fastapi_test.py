# uvicorn fastapi_test:app --host 10.233.202.137 --port 7767
from fastapi import FastAPI,Request, APIRouter,Query
from fastapi import Depends
from typing import List, Optional
import time
from datetime import datetime
from sqlalchemy.orm import Session
import codecs
from create_db import *

from typing import List, Dict, Optional, Type, TypeVar, Generic
from pydantic import BaseModel #具有验证功能，确保不会出现意料之外的字段和应该出现的字段而不存在
from datetime import datetime
from sqlalchemy import asc, desc

################################################################################
################################ 数据库操作 ####################################
################################################################################
from sqlalchemy import create_engine, Column
from sqlalchemy import Integer, String, MetaData,SmallInteger,Date,Text,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import or_, and_

class BaseInfo(BaseModel):
    relations:str       #关系
    health_status:str   #健康状况
    maritalStatus:str   #婚姻状况
    monthIncome:Optional[int]=None     #月工资
    yearIncome: Optional[int]=None     #年工资
    work_type:Optional[str]=None       #工作类型

class Parents(BaseInfo):
    work_city:Optional[str]=None       #工作城市

class Brothers(BaseInfo):
    pass

class Children(BaseModel):
    children_relations:str      #关系
    sex:str            #性别
    children_age: int           #年龄
    children_around:str         #是否在身边
    children_support_payment:str#对方是否出抚养费
    other: Optional[str]=None  #其他补充信息
class HouseAndCar(BaseModel):
    house_loan: str #贷款情况
    is_me:str       #资产是否在自己名下
    address: str    #地址或者品牌

class Information(BaseModel):
    sex:str                     #年龄
    birthDate: str              #出生日期
    address: str                #家庭住址
    # appearance: str             #相貌情况
    # maritalStatus: str          #婚姻状况
    # photos: Optional[List] = None       #照片列表
    # photos_public: Optional[str] = None  #照片是否公开
    # height: int                 #身高
    # weight: int                 #体重
    # monthIncome: int            #月收入
    # yearIncome: int             #年收入
    # workType: str               #工作类型
    # workCity: str               #工作城市
    # workUnit: str               #公司地址
    # education: str              #学历
    # school: str                 #学校名称
    # house_info: List[HouseAndCar]   #房产情况
    # cars: List[HouseAndCar]         #车子情况
    # temperament: Optional[str] = None          #性格
    # other: Optional[str] = None                #其他
    # # parents: Optional[List[Parents]] = []      #父亲情况
    # # brothers: Optional[List[Brothers]] = []    #兄弟姐妹情况
    # # childrens:Optional[List[Children]] = []    #子女情况
    # parents: Optional[List[Parents]]      #父亲情况
    # brothers: Optional[List[Brothers]]    #兄弟姐妹情况
    # childrens:Optional[List[Children]]    #子女情况

# 基类
Base = declarative_base()
# 创建数据库连接和会话
DATABASE_URL = "sqlite:///./yuan.db"  # 示例使用 SQLite，您可以根据需要更改
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()
# 定义泛型变量
T = TypeVar("T", bound=Base)
# 定义通用CRUD类
# 提取公共函数
def build_conditions(search_criteria: Dict[str, List[tuple[str, any]]], model: Type) -> List:
    conditions = []
    for field, criteria in search_criteria.items():
        field_conditions = []
        for op, value in criteria:
            if op == 'gt':
                field_conditions.append(getattr(model, field) > value)
            elif op == 'lt':
                field_conditions.append(getattr(model, field) < value)
            elif op == 'gte':
                field_conditions.append(getattr(model, field) >= value)
            elif op == 'lte':
                field_conditions.append(getattr(model, field) <= value)
            elif op == 'eq':
                field_conditions.append(getattr(model, field) == value)
            else:
                raise ValueError(f"Unsupported operator: {op}")
        if len(field_conditions) > 1:
            conditions.append(and_(*field_conditions))
        else:
            conditions.extend(field_conditions)
    return conditions

class CRUDGeneric(Generic[T]):
    '''
    在SQLAlchemy中，search_mode可以对应于不同的查询方法，这些方法用于匹配不同的搜索需求。以下是一些常用的搜索模式：
    ilike：不区分大小写的模糊匹配（类似于SQL中的ILIKE或LIKE）。
    eq：精确匹配（等于），对应于SQL中的=。
    ne：不等于，对应于SQL中的<>或!=。
    lt：小于，对应于SQL中的<。
    gt：大于，对应于SQL中的>。
    le：小于等于，对应于SQL中的<=。
    ge：大于等于，对应于SQL中的>=。
    in_：在给定的列表中，对应于SQL中的IN。
    not_in：不在给定的列表中，对应于SQL中的NOT IN。
    like：区分大小写的模糊匹配（类似于SQL中的LIKE）。
    contains：字符串是否包含子串，对于集合类型可能表示元素是否在集合中。
    startswith：字符串是否以特定子串开始。
    endswith：字符串是否以特定子串结束。
    match：全文匹配，可能涉及到特定的全文搜索引擎。
    regexp：正则表达式匹配。
    '''
    def __init__(self, model: Type[T]):
        self.model = model

    def numeric_field_search(self,db: Session, field):
        '''
        @功能    :   数值类型的字段搜索
        这里针对年龄的实例
        # 查询年龄大于20且小于30的用户
        query = db.query(self.model).filter(self.model.age > 20, self.model.age < 30).all()
        # 查询年龄在20到30之间的用户（包括20和30）
        query = db.query(self.model).filter(self.model.age.between(20, 30)).all()
        # 查询年龄为25、30或35的用户
        query = db.query(self.model).filter(self.model.age.in_([25, 30, 35])).all()
        # 查询年龄大于20且小于30，或者年龄等于25的用户
        query = db.query(self.model).filter((self.model.age > 20, self.model.age < 30) | (self.model.age == 25)).all()
        '''
        # 查询年龄大于等于20且小于等于30的用户
        query = db.query(self.model).filter(self.model[field] >= 20, self.model[field] <= 30).all()
        # 查询年龄大于等于20的用户
        query = db.query(self.model).filter(self.model[field] >= 20, self.model[field] <= 30).all()
        # 查询年龄小于等于30的用户
        query = db.query(self.model).filter(self.model[field] >= 20, self.model[field] <= 30).all()
        
        # 查询年龄在大于等于20到小于等于30之间的用户
        query = db.query(self.model).filter(self.model[field].between(20, 30)).all()
        # 查询年龄为25、30或35的用户
        query = db.query(self.model).filter(self.model[field].in_([25, 30, 35])).all()
        # 查询年龄大于20且小于30，或者年龄等于25的用户
        query = db.query(self.model).filter((self.model[field] > 20, self.model[field] < 30) | (self.model[field] == 25)).all()
        pass

    def create(self, db: Session, **kwargs)-> T:
        ''' 插入一条数据 '''
        # 调用方式1 ：user_crud.create(db, name="John Doe", age=30)
        # data = {name="John Doe", age=30}
        # 调用方式2 ：user_crud.create(db, **data)
        obj = self.model(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def create_many(self, db: Session, data: List[dict])-> List[T]:
        ''' 批量插入数据 '''
        objects = [self.model(**item)for item in data]
        db.add_all(objects)
        db.commit()
        # db.refresh(objects)
        # return objects
        # 不需要对列表调用 refresh，而是查询最新的对象状态
        return [db.query(self.model).get(obj.id)for obj in objects]

    def read_all(self, db: Session, 
                 id: int=None,
                 offset: int = 0, limit: Optional[int] = None,
                 order_fields: Optional[List[tuple[str, str]]] = None
                 )-> List[T]:
        '''获得所有数据，并且动态根据limit确定获取多少数据'''
        query = db.query(self.model)
        if id is not None:
            return query.filter(self.model.id == id).all()
        # 如果提供了排序字段列表，则应用排序
        query = self.order_by_data(query, order_fields)
        query = self.offset_and_limit(query, offset, limit)
        return query.all()

    def update_dict(self, db: Session, id: int, data_dict:dict)-> T:
        # 调用方法:crud.update(db_session, 1, {name='John Doe'})
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            for key, value in data_dict.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            return obj
        else:
            return None

    def delete(self, db: Session, id: int)-> T:
        '''根据id删除一条数据'''
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return obj
        else:
            return None
        
    def search_by_value(self, db: Session, value: str,
                        offset: int = 0, limit: Optional[int] = None,) -> List[T]:
        """
        基于值对表中所有字段进行搜索
        
        :param db: SQLAlchemy Session对象，用于数据库操作
        :param value: 要搜索的值
        :return: 模型实例列表
        """
        query = db.query(self.model)
        conditions = []

        # 遍历模型的所有字段
        for field_name in self.model.__table__.columns.keys():
            column = getattr(self.model, field_name)
            field_type = column.type
            # 检查字段类型并应用适当的比较操作
            if isinstance(field_type, (String, Text)):
                # 字符串类型的字段使用ilike
                conditions.append(column.ilike(f"%{value}%"))
            elif isinstance(field_type, Integer):
                # 尝试将value转换为整数
                try:
                    conditions.append(column == int(value))
                except ValueError:
                    # 如果value不能转换为整数，忽略这个字段
                    continue
            # 可以添加更多的字段类型检查和相应的比较操作

        if conditions:
            query = query.filter(or_(*conditions))
        # 计算偏移之前的数据总量
        total_count = query.count()
        query = self.offset_and_limit(query, offset=offset, limit=limit)
        return query.all(), total_count
    
    def search_multi_table(self, db: Session, models: List[Type[T]], 
                          search_field: str, search_queries: List[str], 
                          search_mode: str = 'ilike', combine_mode: str = 'or',
                          offset: int = 0, limit: Optional[int] = None,
                          order_fields: Optional[List[tuple[str, str]]] = None
                          ) -> List[T]:
        """
        添加对多张表的一个字段多个值的批量搜索
        :param db: SQLAlchemy Session对象，用于数据库操作
        :param models: 要搜索的模型列表
        :param search_field: 要搜索的字段名称
        :param search_queries: 搜索查询词列表
        :param search_mode: 搜索模式（'ilike' 或 'eq'）
        :param offset: 偏移量，指定跳过多少条记录（默认为0）
        :param limit: 最大返回记录数（默认为None，即无限制）
        :param combine_mode: 组合多个搜索查询的方式，'or' 或 'and'
        :paramorder_fields: 对N个排序字段的每个字段进行排序，[('name', 'asc'), ('age', 'desc')]
        :return: 一个字典，键为模型类型，值为对应模型的查询结果列表
        """
        all_results = {}
        for model in models:
            query = db.query(model)
            conditions = []
            for query_value in search_queries:
                if search_mode == 'ilike':
                    condition = getattr(model, search_field).ilike(f"%{query_value}%")
                elif search_mode == 'eq':
                    condition = getattr(model, search_field) == query_value
                else:
                    raise ValueError(f"Unsupported search mode: {search_mode}")
                conditions.append(condition)
            
            query = self.and_or(query, combine_mode, conditions)

            query = self.order_by_data(query, order_fields)
            query = self.offset_and_limit(query, offset, limit)
            all_results[model] = query.all()
        return all_results
    
    # 添加对多张表的一个字段多个值的批量搜索
    def multi_table_multi_field_multi_value_search(self, 
                        db: Session, models: List[Type[T]], 
                         search_criteria: Dict[str, List[List[str]]], 
                         search_mode: str = 'ilike', 
                         combine_mode: str = 'or',
                         offset: int = 0, 
                         limit: Optional[int] = None,
                         order_fields: Optional[List[tuple[str, str]]] = None
                         ) -> Dict[Type[T], List[T]]:
        """
        添加对多张表的多个字段多个值的批量搜索
        :param db: SQLAlchemy Session对象，用于数据库操作
        :param models: 要搜索的模型列表
        :param search_criteria: 搜索条件字典，键为字段名，值为包含多个搜索词的列表
        :param search_mode: 搜索模式（'ilike' 或 'eq'）
        :param combine_mode: 组合多个搜索查询的方式，'or' 或 'and'
        :param offset: 偏移量，指定跳过多少条记录（默认为0）
        :param limit: 最大返回记录数（默认为None，即无限制）
        :param order_fields: 对N个排序字段的每个字段进行排序，[('name', 'asc'), ('age', 'desc')]
        :return: 一个字典，键为模型类型，值为对应模型的查询结果列表
        """
        all_results = {}
        for model in models:
            query = db.query(model)
            conditions = []
            for field, query_values in search_criteria.items():
                field_conditions = []
                for query_value in query_values:
                    if search_mode == 'ilike':
                        field_conditions.append(getattr(model, field).ilike(f"%{query_value}%"))
                    elif search_mode == 'eq':
                        field_conditions.append(getattr(model, field) == query_value)
                    else:
                        raise ValueError(f"Unsupported search mode: {search_mode}")
                if combine_mode.lower() == 'and':
                    conditions.append(and_(*field_conditions))
                else:
                    conditions.append(or_(*field_conditions))
            
            query = self.and_or(query, combine_mode, conditions)
            query = self.order_by_data(query, order_fields)
            query = self.offset_and_limit(query, offset, limit)
            all_results[model] = query.all()
        return all_results
    
    def multi_field_multi_value_search(self, db: Session, 
                           search_criteria: Dict[str, List[str]]=None, 
                           search_mode: str = 'ilike',combine_mode: str = 'and',
                           offset: int = 0, limit: Optional[int] = None,
                          order_fields: Optional[List[tuple[str, str]]] = None
                           )-> List[T]:
        """
        多个字段，字段多个值的文本搜索
        扩展搜索功能以支持字典形式的参数、不同的搜索模式，并支持分页
        :param db: SQLAlchemy Session对象，用于数据库操作
        :param search_criteria: 搜索条件字典，键为字段名，值为搜索词列表
        :param search_mode: 搜索模式（'ilike' 或 'eq'）
        :param offset: 偏移量，指定跳过多少条记录（默认为0）
        :param limit: 最大返回记录数（默认为None，即无限制）
        :param combine_mode: 组合多个搜索条件的方式，'or' 或 'and'
        :paramorder_fields: 对N个排序字段的每个字段进行排序，[('name', 'asc'), ('age', 'desc')]
        :return: 模型实例列表
        实例：
        # 创建CRUD实例
        user_crud = CRUDGeneric(User)
        # 使用CRUD实例
        db = SessionLocal()
        # 单字段多个值搜索，使用ilike模式
        search_results_single_field_multi_values = user_crud.multi_field_multi_value_search(db, {"name": ["John", "Jane"]}, search_mode='ilike')
        # 打印搜索结果
        for user in search_results_single_field_multi_values:
            print(f"User: {user.name}, Age: {user.age}")
        # 多字段单个值搜索，使用eq模式
        search_results_multi_fields_single_values = user_crud.multi_field_multi_value_search(db, {"name": "John", "age": 30}, search_mode='eq')
        # 打印搜索结果
        for user in search_results_multi_fields_single_values:
            print(f"User: {user.name}, Age: {user.age}")
        # 多字段多个值搜索，使用ilike模式
        search_results_multi_fields_multi_values = user_crud.multi_field_multi_value_search(db, {"name": ["John", "Jane"], "age": [25, 30]}, search_mode='ilike')
        # 打印搜索结果
        for user in search_results_multi_fields_multi_values:
            print(f"User: {user.name}, Age: {user.age}")
        """

        query = db.query(self.model)
        if search_criteria is None or not search_criteria:
            query = self.offset_and_limit(query, offset, limit)
            return query.all()

        conditions = []
        for field, values in search_criteria.items():
            if not isinstance(values, list):
                values = [values]  # 确保值是列表
            field_conditions = []
            for value in values:
                if search_mode == 'ilike':
                    field_conditions.append(getattr(self.model, field).ilike(f"%{value}%"))
                elif search_mode == 'eq':
                    field_conditions.append(getattr(self.model, field) == value)
                else:
                    raise ValueError(f"Unsupported search mode: {search_mode}")
            if combine_mode.lower() == 'and':
                conditions.append(and_(*field_conditions))
            else:
                conditions.append(or_(*field_conditions))

        query = self.and_or(query, combine_mode, conditions)

        # 如果提供了排序字段列表，则应用排序
        query = self.order_by_data(query, order_fields)
        query = self.offset_and_limit(query, offset, limit)

        return query.all()
    
    def FlexibleNumericSearch(self, db: Session, 
                             search_criteria: Dict[str, List[tuple[str, float]]], 
                             combine_mode: str = 'and',
                             offset: int = 0, 
                             limit: Optional[int] = None,
                             order_fields: Optional[List[tuple[str, str]]] = None
                             ) -> List[T]:
        """
        扩展搜索功能以支持数字字段的灵活搜索
        :param db: SQLAlchemy Session对象，用于数据库操作
        :param search_criteria: 数字搜索条件字典，键为字段名，值为操作符和值的列表
        :param combine_mode: 组合多个搜索条件的方式，'or' 或 'and'
        :param offset: 偏移量，指定跳过多少条记录（默认为0）
        :param limit: 最大返回记录数（默认为None，即无限制）
        :param order_fields: 对N个排序字段的每个字段进行排序，[('name', 'asc'), ('age', 'desc')]
        :return: 模型实例列表
        """
        query = db.query(self.model)
        if not search_criteria:
            query = self.offset_and_limit(query, offset, limit)
            return query.all()

        conditions = []
        for field, criteria in search_criteria.items():
            field_conditions = []
            for op, value in criteria:
                if op == 'gt':  # 大于
                    field_conditions.append(getattr(self.model, field) > value)
                elif op == 'lt':  # 小于
                    field_conditions.append(getattr(self.model, field) < value)
                elif op == 'gte':  # 大于等于
                    field_conditions.append(getattr(self.model, field) >= value)
                elif op == 'lte':  # 小于等于
                    field_conditions.append(getattr(self.model, field) <= value)
                elif op == 'eq':  # 等于
                    field_conditions.append(getattr(self.model, field) == value)
                else:
                    raise ValueError(f"Unsupported operator: {op}")
            if len(field_conditions) > 1 and combine_mode.lower() == 'and':
                conditions.append(and_(*field_conditions))
            else:
                conditions.append(or_(*field_conditions))

        if len(conditions) > 1 and combine_mode.lower() == 'and':
            query = query.filter(and_(*conditions))
        else:
            query = query.filter(or_(*conditions))

        # 如果提供了排序字段列表，则应用排序
        query = self.order_by_data(query, order_fields)
        query = self.offset_and_limit(query, offset, limit)
        return query.all()
    
    def order_by_data(self,query, order_fields):
        '''
        @Time    :   2024/11/28 11:49:36
        @功能    :   对数据库进行排序
        '''
        if order_fields:
            for field, direction in order_fields:
                if direction.lower() == 'desc':
                    query = query.order_by(desc(getattr(self.model, field)))
                else:
                    query = query.order_by(asc(getattr(self.model, field)))
        return query
    
    def offset_and_limit(self, query, offset, limit):
        '''
        @Time    :   2024/11/28 11:51:31
        @功能    :   返回指定位置开始的指定数据量
        '''
        query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query
    
    def and_or(self, query, combine_mode, conditions):
        '''
        @Time    :   2024/11/28 11:59:11
        @功能    :   None
        '''
        if combine_mode.lower() == 'and':
            query = query.filter(and_(*conditions))
        else:
            query = query.filter(or_(*conditions))
        return query
    
# 使用CRUDGeneric类

# 创建依赖项函数来获取数据库会话
def get_db():
    # db 会话会在完成一次请求结束之后自动关闭
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 定义模型
class InformationTable(Base):
    # 个人基本信息表
    __tablename__ = "information"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '个人基本信息.'}},)  # 表级别的文档说明
    '''在 SQLAlchemy 中，`Column` 是用于定义表中列的基本对象。以下是 `Column` 的一些常用参数及其作用：
    1. **`type_`**：这是最重要的参数，用于指定列的数据类型。例如，`String`、`Integer`、`Float` 等。
    2. **`nullable`**：布尔值，指定列是否可以包含 NULL 值，默认为 `True`。如果设置为 `False`，则列不能包含 NULL 值。
    3. **`default`**：指定列的默认值。如果未指定，且数据库列允许 NULL 值，则默认值为 NULL；如果不允许 NULL 值，则必须在应用层指定默认值。
    4. **`index`**：布尔值或名称，如果为 `True`，则创建一个索引在该列上。也可以是一个字符串，表示索引的名称。
    5. **`primary_key`**：布尔值，如果为 `True`，则该列是表的主键的一部分。
    6. **`foreign_key`**：字符串或约束对象，用于指定外键约束，关联到另一个表的列。
    7. **`unique`**：布尔值，如果为 `True`，则创建一个唯一约束在该列上，确保列中的所有值都是唯一的。
    8. **`autoincrement`**：布尔值，通常与整数主键一起使用，指定该列的值是否应该自动递增。
    9. **`doc`**：字符串，用于提供列的文档字符串，这在生成文档时非常有用。
    10. **`key`**：字符串，用于指定列的标签名，这在 ORM 操作中特别有用。
    11. **`comment`**：字符串，用于为列添加注释，这在数据库中创建列时会使用。
    12. **`onupdate`**：值或 callable，指定在更新操作时该列应该采取的动作，例如可以设置为当前的时间戳。
    13. **`server_default`**：服务器默认值，这是一个数据库服务器层面的默认值，不同于应用层的默认值。
    `type_`、`nullable`、`default` 和 `index` 是最重要的参数，因为它们直接影响列的数据库定义和行为。其他参数则提供了额外的灵活性和约束，以满足不同的业务需求和数据库设计考虑。
    '''
    '''
    在 SQLAlchemy 中，`Column` 的 `type_` 参数可以是 SQLAlchemy 类型系统的一部分，这些类型对应于数据库中的原生数据类型。以下是一些常用的 SQLAlchemy 类型及其对应的数据库类型：
    1. **`Integer`**：对应于数据库的整型。
    2. **`SmallInteger`**：对应于数据库的小整型。
    3. **`BigInteger`**：对应于数据库的大整型。
    4. **`Float`**：对应于数据库的浮点型。
    5. **`Numeric`**（或 `DECIMAL`）：对应于数据库的定点数类型，可以指定精度和小数点后的位数。
    6. **`String`**：对应于数据库的字符串类型，可以指定长度。
    7. **`Text`**：对应于数据库的文本类型，用于存储大量文本。
    8. **`Boolean`**：对应于数据库的布尔类型。
    9. **`Date`**：对应于数据库的日期类型。
    10. **`Time`**：对应于数据库的时间类型。
    11. **`DateTime`**：对应于数据库的日期时间类型。
    12. **`Enum`**：对应于数据库的枚举类型，可以限制列只能包含预定义的值。
    13. **`PickleType`**：用于将 Python 对象序列化为字符串并存储在数据库中，但通常不推荐使用，因为它不是安全或高效的。
    14. **`LargeBinary`**：对应于数据库的大二进制类型，用于存储大量二进制数据。
    15. **`Binary`**：对应于数据库的二进制类型。
    16. **`JSON`**：对应于数据库的 JSON 类型，用于存储 JSON 数据。
    17. **`UUID`**：对应于数据库的 UUID 类型。
    这些类型是 SQLAlchemy 内置的，但您也可以使用数据库特定的类型，或者自定义类型。例如，PostgreSQL 有它自己的一系列类型，如 `ARRAY`、`HSTORE`、`JSONB` 等，这些可以通过 `postgresql` 前缀来使用，如 `postgresql.ARRAY`、`postgresql.HSTORE`、`postgresql.JSONB`。
    选择正确的类型对于确保数据的完整性和应用的性能至关重要。在使用时，您应该根据您的具体需求和数据库的支持来选择最合适的类型。
    '''

    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    name = Column( String,index=True, doc="",comment="")
    sex = Column( String,index=True, doc="",comment="")
    birthDate = Column( Date,index=True, doc="出生日期",comment="出生日期")
    age = Column( SmallInteger,index=True, doc="",comment="")
    address = Column( String,index=True, doc="现在的家庭住址",comment="现在的家庭住址")
    photos = Column( String,index=True, doc="照片列表",comment="照片列表")
    Hope_settle_city = Column( String,index=True, doc="希望定居的城市",comment="希望定居的城市")
    temperament = Column( String,index=True, doc="性格",comment="性格")
    appearance = Column( String,index=True, doc="容貌情况",comment="容貌情况")
    maritalStatus = Column( String,index=True, doc="婚姻状况",comment="婚姻状况")
    height = Column( SmallInteger,index=True, doc="身高单位CM",comment="身高单位CM")
    weight = Column( SmallInteger,index=True, doc="体重单位KG",comment="体重单位KG")
    drinking = Column( String,index=True, doc="喝酒情况",comment="喝酒情况")
    smorking = Column( String,index=True, doc="吸烟情况",comment="吸烟情况")
    monthIncome = Column( SmallInteger,index=True, doc="月收入单位人民币元",comment="月收入单位人民币元")
    yearIncome = Column( SmallInteger,index=True, doc="年收入单位人民万元",comment="年收入单位人民万元")
    bank_deposit = Column( SmallInteger,index=True, doc="存款单位人民万元",comment="存款单位人民万元")
    workType = Column( String,index=True, doc="工作类型",comment="工作类型")
    workCity = Column( String,index=True, doc="工作城市",comment="工作城市")
    workUnit = Column( String,index=True, doc="工作单位",comment="工作单位")
    education = Column( Text,index=True, doc="学历",comment="学历")
    major = Column( Text,index=True, doc="专业",comment="专业")
    school = Column( String,index=True, doc="最后学历的学校",comment="最后学历的学校")
    educational_supplements = Column( Text,index=True, doc="教育经历补充",comment="教育经历补充")
    childrens_number = Column( SmallInteger,index=True, doc="子女数量",comment="子女数量")
    hobbies = Column( String,index=True, doc="爱好",comment="爱好")
    houses = Column( SmallInteger,index=True, doc="房子数量",comment="房子数量")
    house_loan = Column( String,index=True, doc="房子贷款情况",comment="房子贷款情况")
    cars = Column( SmallInteger,index=True, doc="车子数量",comment="车子数量")
    car_loan = Column( String,index=True, doc="车子贷款情况",comment="车子贷款情况")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")

    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AssetTable(Base):
    # 资产信息表
    __tablename__ = "asset"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '个人资产情况.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    asset_type = Column( Integer,index=True, doc="资产类型。0 表示房产；1 表示车. 如果选择0则车品牌默认将被设置为空；反之 城市和详细地址将被设置为空",comment="资产类型。0 表示房产；1 表示车. 如果选择0则车品牌默认将被设置为空；反之 城市和详细地址将被设置为空")
    is_loan = Column( String,index=True, doc="是否有贷款",comment="是否有贷款")
    is_me = Column( String,index=True, doc="是否在我名下",comment="是否在我名下")
    city = Column( String,index=True, doc="房子所在城市",comment="房子所在城市")
    address = Column( String,index=True, doc="房子详细地址",comment="房子详细地址")
    brand = Column( String,index=True, doc="汽车品牌",comment="汽车品牌")
    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class FamilysTable(Base):
    # 父母兄弟表
    __tablename__ = "familys"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '个人家庭情况，父母兄弟姐妹.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    relations = Column( String,index=True, doc="关系",comment="关系")
    maritalStatus = Column( String,index=True, doc="婚姻状况",comment="婚姻状况")
    health_status = Column( String,index=True, doc="健康状况",comment="健康状况")
    work_type = Column( String,index=True, doc="工作类型",comment="工作类型")
    work_city = Column( String,index=True, doc="工作城市",comment="工作城市")
    monthIncome = Column( Integer,index=True, doc="月薪，单位人民币元",comment="月薪，单位人民币元")
    yearIncome = Column( Integer,index=True, doc="年薪，单位人民币万元",comment="年薪，单位人民币万元")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ChildrenTable(Base):
    # 子女表
    __tablename__ = "children"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '个人子女情况.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    sex = Column( String,index=True, doc="",comment="")
    age = Column( SmallInteger,index=True, doc="",comment="")
    relations = Column( String,index=True, doc="关系",comment="关系")
    photos = Column( String,index=True, doc="照片列表",comment="照片列表")
    children_around = Column( String,index=True, doc="是否在身边",comment="是否在身边")
    children_support_payment = Column( String,index=True, doc="对方是否出抚养费",comment="对方是否出抚养费")
    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")
    height = Column( SmallInteger,index=True, doc="身高单位CM",comment="身高单位CM")
    weight = Column( SmallInteger,index=True, doc="体重单位KG",comment="体重单位KG")
    education = Column( String,index=True, doc="学历",comment="学历")
    major = Column( String,index=True, doc="专业",comment="专业")
    school = Column( String,index=True, doc="最后学历的学校",comment="最后学历的学校")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class MatchingSituationTable(Base):
    # 男女匹配情况
    __tablename__ = "matching_situation" 
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '男女匹配情况.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    man_only_key = Column(String ,index=True, doc="数据库中男士唯一的key，基本在所有表中都有使用",comment="数据库中男士唯一的key，基本在所有表中都有使用")
    woman_only_key = Column(String ,index=True, doc="数据库中女士唯一的key，基本在所有表中都有使用",comment="数据库中女士唯一的key，基本在所有表中都有使用")
    matching_only_key = Column( String,index=True, doc="匹配用户唯一标识",comment="匹配用户唯一标识")
    matchmaker = Column( String,index=True, doc="红娘",comment="红娘")
    begin_date = Column( Date,index=True, doc="开始时间",comment="开始时间")
    close_date = Column( Date,index=True, doc="结束时间",comment="结束时间")
    results = Column( String,index=True, doc="结果",comment="结果")
    duration = Column( String,index=True, doc="持续多长时间",comment="持续多长时间")
    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")
    height_difference = Column( String,index=True, doc="身高差",comment="身高差")
    weight_difference = Column( SmallInteger,index=True, doc="体重差",comment="体重差")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class EvaluationTable(Base):
    # 评价表
    __tablename__ = "evaluation" 
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '对某个客户的评论.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    man_only_key = Column(String ,index=True, doc="数据库中男士唯一的key，基本在所有表中都有使用",comment="数据库中男士唯一的key，基本在所有表中都有使用")
    woman_only_key = Column(String ,index=True, doc="数据库中女士唯一的key，基本在所有表中都有使用",comment="数据库中女士唯一的key，基本在所有表中都有使用")
    evaluation_type = Column( Integer,index=True, doc="评价方0 表示:用户对匹配对象的评论； 1 表示:匹配对象对用户的评论；2 表示:红娘对用户的评论",comment="评价方0 表示:用户对匹配对象的评论； 1 表示:匹配对象对用户的评论；2 表示:红娘对用户的评论")
    evaluation = Column( Text,index=True, doc="评价",comment="评价")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RedressTrackTable(Base):
    # 红娘追踪记录
    __tablename__ = "redress_track" 
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ( {'info': {'doc': '匹配成功后，红娘的追踪情况.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    man_only_key = Column(String ,index=True, doc="数据库中男士唯一的key，基本在所有表中都有使用",comment="数据库中男士唯一的key，基本在所有表中都有使用")
    woman_only_key = Column(String ,index=True, doc="数据库中女士唯一的key，基本在所有表中都有使用",comment="数据库中女士唯一的key，基本在所有表中都有使用")
    matching_only_key = Column( String,index=True, doc="匹配用户唯一标识",comment="匹配用户唯一标识")
    matchmaker = Column( String,index=True, doc="红娘",comment="红娘")
    man_date = Column( Date,index=True, doc="和男方沟通时间",comment="和男方沟通时间")
    woman_date = Column( Date,index=True, doc="和女方沟通时间",comment="和女方沟通时间")
    man_results = Column( String,index=True, doc="和男方沟通结果",comment="和男方沟通结果")
    woman_results = Column( String,index=True, doc="和女方沟通结果",comment="和女方沟通结果")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SelectOptions(Base):
    # 项目中使用的下拉列表项
    __tablename__ = "select_options"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '下拉列表项，固定的字段不需要每次关系.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    name = Column(String ,index=True, doc="下拉列表项的名称",comment="下拉列表项的名称")
    items = Column( String,index=True, doc="下拉列表项",comment="下拉列表项")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    desc = Column( String,index=True, doc="下拉列表说明",comment="下拉列表说明")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ShowFields(Base):
    # web显示的字段
    __tablename__ = "show_fields"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '将在web表格中显示的字段.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    fields = Column(String ,index=True, doc="web显示的字段",comment="web显示的字段")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    desc = Column( String,index=True, doc="将在web表格中显示的字段",comment="将在web表格中显示的字段")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class FieldMapping(Base):
    # web表格中的字段和数据库的映射关系
    __tablename__ = "field_mapping"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': 'web表格中的字段和数据库的映射关系.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    web_field = Column(String ,index=True, doc="web显示的字段",comment="web显示的字段")
    table_field = Column(String ,index=True, doc="数据库表中的字段",comment="数据库表中的字段")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    desc = Column( String,index=True, doc="字段介绍",comment="字段介绍")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class UpdateRecordTabel(Base):
    # 对数据库的所有修改的记录
    __tablename__ = "update_record"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '对数据库表中所有的修改都被记录再次，该表数据不允许删除.'}},)  # 表级别的文档说明
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="唯一对于的key",comment="唯一对于的key")
    table_name = Column(String ,index=True, doc="修改的表名称",comment="修改的表名称")
    type = Column(String ,index=True, doc="操作表的动作",comment="操作表的动作")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    update_ip = Column(String ,index=True, default="0.0.0.0",doc="更新时间",comment="更新时间")
    update_owner = Column(String ,index=True, doc="操作人姓名",comment="操作人姓名")
    old_data = Column(Text ,index=True, doc="修改前数据内容",comment="修改前数据内容")
    new_data = Column(Text ,index=True, doc="修改后数据内容",comment="修改后数据内容")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RequestTable(Base):
    '''个人要求信息，所有范围值都使用 ;; 两个作为连接符'''
    __tablename__ = "request"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '个人要求信息'}},)  # 表级别的文档说明
    
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    sex = Column( String,index=True, doc="",comment="")
    birthDate_range = Column( String,index=True, doc="出生日期范围",comment="出生日期范围")
    age_range = Column( String,index=True, doc="年龄范围",comment="年龄范围")
    photos_public = Column( String,index=True, doc="照片是否公开",comment="照片是否公开")
    Hope_settle_city = Column( String,index=True, doc="希望定居的城市列表",comment="希望定居的城市列表")
    temperament = Column( String,index=True, doc="性格列表",comment="性格列表")
    appearance = Column( String,index=True, doc="容貌情况列表",comment="容貌情况列表")
    maritalStatus = Column( String,index=True, doc="婚姻状况列表",comment="婚姻状况列表")
    height_range = Column( String,index=True, doc="身高范围单位CM",comment="身高范围单位CM")
    weight_range = Column( String,index=True, doc="体重范围单位KG",comment="体重范围单位KG")
    drinking = Column( String,index=True, doc="喝酒情况列表",comment="喝酒情况列表")
    smorking = Column( String,index=True, doc="吸烟情况列表",comment="吸烟情况列表")
    monthIncome_range = Column( String,index=True, doc="月收入范围单位人民币元",comment="月收入范围单位人民币元")
    yearIncome_range = Column( String,index=True, doc="年收入范围单位人民万元",comment="年收入范围单位人民万元")
    bank_deposit_range=Column( String,index=True, doc="存款范围单位人民万元",comment="存款范围单位人民万元")
    workType = Column( String,index=True, doc="工作类型列表",comment="工作类型列表")
    workCity = Column( String,index=True, doc="工作城市列表",comment="工作城市列表")
    workUnit = Column( String,index=True, doc="工作单位列表",comment="工作单位列表")
    academic_qualifications = Column( Text,index=True, doc="学历列表",comment="学历列表")
    major = Column( Text,index=True, doc="专业列表",comment="专业列表")
    school = Column( String,index=True, doc="最后学历的学校类型（985 211 普通等等）列表",comment="最后学历的学校类型（985 211 普通等等）列表")
    educational_supplements = Column( Text,index=True, doc="教育经历补充",comment="教育经历补充")
    childrens_number = Column( String,index=True, doc="子女数量范围",comment="子女数量范围")
    hobbies = Column( String,index=True, doc="爱好列表",comment="爱好列表")
    # houses = Column( String,index=True, doc="是否有房子，可以输入数量",comment="是否有房子，可以输入数量")
    # house_loan = Column( String,index=True, doc="房子贷款情况列表",comment="房子贷款情况列表")
    # cars = Column( String,index=True, doc="是否有车子，可以输入数量",comment="是否有车子，可以输入数量")
    # car_loan = Column( String,index=True, doc="车子贷款情况列表",comment="车子贷款情况列表")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RequestFamilysTable(Base):
    '''对于另一半家庭要求信息，所有范围值都使用 ;; 两个作为连接符'''
    __tablename__ = "request_familys"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ( {'info': {'doc': '对于另一半家庭要求信息，所有范围值都使用 ;; 两个作为连接符'}},)  # 表级别的文档说明
    
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    relations = Column( String,index=True, doc="关系",comment="关系")
    maritalStatus = Column( String,index=True, doc="婚姻状况列表",comment="婚姻状况列表")
    health_status = Column( String,index=True, doc="健康状况列表",comment="健康状况列表")
    work_type = Column( String,index=True, doc="工作类型列表",comment="工作类型列表")
    work_city = Column( String,index=True, doc="工作城市列表",comment="工作城市列表")
    monthIncome_range = Column( String,index=True, doc="月收入范围单位人民币元",comment="月收入范围单位人民币元")
    yearIncome_range = Column( String,index=True, doc="年收入范围单位人民万元",comment="年收入范围单位人民万元")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class RequestAssetTable(Base):
    '''对于另一半家庭要求信息，所有范围值都使用 ;; 两个作为连接符'''
    __tablename__ = "request_asset"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ( {'info': {'doc': '对于另一半个人资产要求信息，所有范围值都使用 ;; 两个作为连接符'}},)  # 表级别的文档说明
    
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    asset_type = Column( Integer,index=True, doc="资产类型。0 表示房产；1 表示车. 如果选择0则车品牌默认将被设置为空；反之 城市和详细地址将被设置为空",comment="资产类型。0 表示房产；1 表示车. 如果选择0则车品牌默认将被设置为空；反之 城市和详细地址将被设置为空")
    assets_number = Column( Integer,index=True, doc="资产数量")
    is_loan = Column( String,index=True, doc="是否有贷款",comment="是否有贷款")
    is_me = Column( String,index=True, doc="是否在我名下",comment="是否在我名下")
    city = Column( String,index=True, doc="房子所在城市",comment="房子所在城市")
    address = Column( String,index=True, doc="房子详细地址",comment="房子详细地址")
    brand = Column( String,index=True, doc="汽车品牌",comment="汽车品牌")
    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ReeuestChildrenTable(Base):
    # 对于另一半的要求子女表
    __tablename__ = "request_children"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = ({'info': {'doc': '对于另一半的要求子女的要求.'}},)  # 表级别的文档说明
    
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    sex = Column( String,index=True, doc="",comment="")
    age_range = Column( String,index=True, doc="年龄范围",comment="年龄范围")
    relations = Column( String,index=True, doc="关系",comment="关系")
    photos_public = Column( String,index=True, doc="照片是否公开",comment="照片是否公开")
    children_around = Column( String,index=True, doc="是否在身边",comment="是否在身边")
    children_support_payment = Column( String,index=True, doc="对方是否出抚养费",comment="对方是否出抚养费")
    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 创建每一张表的CRUD实例
information_crud = CRUDGeneric(InformationTable)    # 个人基本信息表CRUD实例
asset_crud = CRUDGeneric(AssetTable)        # 资产信息表CRUD实例
familys_crud = CRUDGeneric(FamilysTable)    # 父母兄弟表CRUD实例
children_crud = CRUDGeneric(ChildrenTable)  # 子女表CRUD实例
match_crud = CRUDGeneric(MatchingSituationTable)    # 男女匹配情况CRUD实例
select_crud = CRUDGeneric(SelectOptions)    # 项目中使用的下拉列表项CRUD实例
show_filed_crud = CRUDGeneric(ShowFields)   # web显示的字段CRUD实例
fieldmapping_crud = CRUDGeneric(FieldMapping)       # web表格中的字段和数据库的映射关系CRUD实例
redress_crud = CRUDGeneric(RedressTrackTable)       # 红娘追踪记录CRUD实例
evaluation_crud = CRUDGeneric(EvaluationTable)      # 评价表CRUD实例
update_record_crud = CRUDGeneric(UpdateRecordTabel) # 对数据库的所有修改的记录CRUD实例
request_crud = CRUDGeneric(RequestTable)   # 个人要求表
request_asset_crud = CRUDGeneric(RequestAssetTable)         # 个人要求表
request_familys_crud = CRUDGeneric(RequestFamilysTable)     # 个人对家庭的要求表
request_children_crud = CRUDGeneric(ReeuestChildrenTable)   # 个人子女的要求表

select_options = {
    "work_type_arr":{
        "list":["务农","公务员","教师","医生","护士","独立创业者","科技工作者","金融工作者"],
        "desc":"工作类型"
    },
    "marital_status_arr":{
        "list":["未婚","离异","丧偶"],
        "desc":"婚姻状况"
    },
    "borthers_marital_status":{
        "list":["已婚","未婚","离异","丧偶"],
        "desc":"婚姻状况"
    },
    "academic_qualifications_arr":{
        "list":["初中","高中","职高","中/大专","本科","研究生","博士","博士后"],
        "desc":"教育程度"
    },
    "brothers_arr":{
        "list":["哥哥","姐姐","弟弟","妹妹"],
        "desc":"兄弟姐妹关系"
    },
    "asset_loan_arr":{
        "list":["无贷款","有贷款","随时可以买","无"],
        "desc":"个人资产的几种状态"
    },
    "parents_work_status_arr":{
        "list":["退休","教师","公职人员","医护人员","打工","个体户","务农","不便透露"],
        "desc":"父母的工作类型"
    },
    "sex_arr":{
        "list":["男", "女"],
        "desc":"性别"
    },
    "appearance_arr":{
        "list":["一般", "普通", "姣好"],
        "desc":"容貌描述"
    },
    "temperament_arr":{
        "list":["外向","内向","乐观","悲观","积极","消极","开朗","严肃","幽默","随和","固执","灵活","死板","冷静","冲动",
        "谨慎","细心","大意","负责","轻率","可靠","耐心","急躁","勤奋","懒惰","诚实","虚伪","真诚","做作","独立","依赖",
        "自信","自卑","谦逊","傲慢","有野心","随遇而安","好奇","热情","冷淡","有创造力","保守","有条理","有同情心","复合型人格"],
        "desc":"性格下拉选项，这个大概率应该用来手写"
    },
    "health_status_arr":{
        "list":["健康","亚健康","有残疾","已故"],
        "desc":"身体情况"
    },
    "request_arr_prefix":{
        "list":["无要求"],
        "desc":"提要求的时候有这个选项前缀"
    },
    "information_arr_suffix":{
        "list":["不便说"],
        "desc":"填写自己信息的时候提供这个选项后缀"
    },
    "drinking_arr":{
        "list":["喝酒","不喝酒","偶尔喝酒"],
        "desc":""
    },
    "smorking_arr":{
        "list":["抽烟","抽烟","偶尔抽烟"],
        "desc":""
    },
    "hobbies_arr":{
        "list":["旅游","滑雪","烧菜","看书","书法","钓鱼"],
        "desc":"个人爱好"
    }
}

# 组织所有的下拉列表项
select_options_list = []
number = 0
for key, value_dict in select_options.items():
    select_options_list.append({
        "id":number,
        "name":key,
        "items":str(value_dict['list']),
        "desc":value_dict['desc']
     })
    number += 1
# 组织所有将在表格中显示的字段
show_fields_list=[{
    "id":0,
    # "fields":'["姓名","性别","住址","婚姻状况","出生日期","年龄","外貌","性格","身高","体重","学历","专业","学校","房产贷款","所在城市","详细地址","车贷款","品牌","月收入","年收入","工作类型","工作城市","希望定居城市","兴趣爱好","是否喝酒","是否吸烟"]',
    "fields":'["姓名","性别","住址","婚姻状况","出生日期","年龄","外貌","性格","身高","体重","学历","专业","学校","房产(套)","贷款(房)","在我名下(房)","车(辆)","贷款(车)","在我名下(车)","年收入","工作类型","工作城市","希望定居城市","兴趣爱好","是否喝酒","是否吸烟","兄弟姐妹(数量)"]',
    "desc":"将在表格中显示的字段"
}]
# 组织所有的下拉列表项
fieldMapping_dict= {
    "id": "id",
    "用户唯一标识": "onlyKey",
    "姓名": "name",
    "性别": "sex",
    "出生日期": "birthDate",
    "年龄": "age",
    "住址": "address",
    "希望定居城市":"Hope_settle_city",
    "外貌": "appearance",
    "性格": "temperament",
    "婚姻状况": "maritalStatus",
    # "照片": "photos",
    # "照片列表": "photosList",
    # "是否公开": "photos_public",
    # "默认显示下标": "photosIndex",
    "身高": "height",
    "体重": "weight",
    "学历": "education",
    "专业": "major",
    "学校": "school",
    "教育经历补充": "educational_supplements",
    "月收入": "monthIncome",
    "年收入": "yearIncome",
    "工作类型": "workType",
    "工作单位": "workUnit",
    "工作城市": "workCity",
    "其他": "other",
    "兴趣爱好": "hobbies",
    "是否喝酒": "drinking",
    "是否吸烟": "smorking",

    # # 房产信息需要从资产表中整合出来
    # 房产 N处， 
    # 贷款：部分有贷款，部分无贷款
    # 自己名下：部分在，部分不在
    # 车子 N辆
    # 贷款：部分有贷款，部分无贷款
    # 自己名下：部分在，部分不在

    # "房产": "house",
    # "房产贷款": "houseLoan",
    # "城市": "houseCity",
    # "详细地址": "houseAddress",
    # "车": "car",
    # "车贷款": "carLoan",
    # "品牌": "carBrands",

    # "家庭情况": "familySituation",
    # "父亲": "father",
    # "父亲是否健康": "fatherHealthy",
    # "父亲是否退休": "fatherRetired",
    # "父亲工作类型": "fatherWork",
    # "父亲月收入": "fatherMonthIncome",
    # "父亲年收入": "fatherYearIncome",
    # "母亲": "mother",
    # "母亲是否健康": "motherHealthy",
    # "母亲是否退休": "motherRetired",
    # "母亲工作类型": "motherWork",
    # "母亲月收入": "motherMonthIncome",
    # "母亲年收入": "motherYearIncome",
    # "兄弟姐妹": "siblings",
    # "兄弟姐妹关系": "siblingsRelationship",
    # "兄弟姐妹婚姻状况": "siblingsMaritalStatus",
    # "兄弟姐妹是否健康": "siblingsHealthy",
    # "兄弟姐妹工作类型": "siblingsWork",
    # "兄弟姐妹月收入": "siblingsMonthIncome",
    # "兄弟姐妹年收入": "siblingsYearIncome"
}

fieldMapping_list, number = [], 0
for key, value in fieldMapping_dict.items():
    fieldMapping_list.append({
        "id":number,
        "web_field":key,
        "table_field":value,
        "desc":"" 
    })
    number += 1

def 向table批量插入数据(db, table, datas):
    '''
    @Time    :   2024/11/22 17:16:22
    @功能    :   None
    '''
    # 创建CRUD实例
    table_crud = CRUDGeneric(table)
    try:
        last_user = db.query(table).order_by(table.id.desc()).first()
        last_id = last_user.id+1
    except:
        last_id = 0
    # for index, data_dict in enumerate(datas):
    #     data_dict["id"] = last_id+index+1
        # datas[index] = data_dict
    new_datas = table_crud.create_many(db, datas)
    return new_datas

# 创建表格
Base.metadata.create_all(bind=engine)
# # 使用CRUD实例
# db = SessionLocal()
# 向table批量插入数据(db, SelectOptions, select_options_list)
# 向table批量插入数据(db, ShowFields, show_fields_list)
# 向table批量插入数据(db, FieldMapping, fieldMapping_list)

def 根据年龄计算出生日期(age):
    '''
    @Time    :   2024/11/28 12:54:58
    @功能    :   根据年龄计算出生日期
    '''
    # 获取当前日期
    当前日期 = datetime.now()
    # 计算出生日期
    出生日期 = 当前日期.replace(year=当前日期.year - age).strftime("%Y-%m-%d")
    return 出生日期

def 根据出生日期计算周岁和虚岁(出生日期):
    '''
    @Time    :   2024/11/06 16:41:28
    @功能    :   None
    出生日期格式："2000-01-01"
    '''
    # 将字符串解析为 datetime 对象
    出生日期 = datetime.strptime(出生日期, "%Y-%m-%d")
    # 获取当前日期
    当前日期 = datetime.now()
    # 计算周岁
    周岁 = 当前日期.year - 出生日期.year - ((当前日期.month, 当前日期.day)< (出生日期.month, 出生日期.day))
    # 计算虚岁
    虚岁 = 周岁 + 1 if (当前日期.month, 当前日期.day)>= (出生日期.month, 出生日期.day)else 周岁
    # print(f"周岁: {周岁}, 虚岁: {虚岁}")
    return {"周岁":周岁,"虚岁":虚岁}

def 生成OnlyKey(data_dict):
    '''
    @Time    :   2024/11/21 14:01:21
    @功能    :   None
    '''
    time_str = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return rf"{data_dict['name']}_{data_dict['birthDate']}_{time_str}"

def 提取个人信息(only_key, data_dict):
    '''
    @Time    :   2024/11/21 13:28:37
    @功能    :   提取个人基本信息
    '''
    keys = ["name","sex","birthDate","address","Hope_settle_city","other",
            "drinking","smorking","appearance","maritalStatus","height","weight","monthIncome","bank_deposit","major",
            "yearIncome","workType","workCity","workUnit","education","school","educational_supplements",
            "childrens_number","hobbies","temperament"]
    age_dict = 根据出生日期计算周岁和虚岁(data_dict['birthDate'])
    information_dict={"id":None,
                "only_key":only_key,
                "age":age_dict['周岁'],
                "photos":[]
                }
    if "id" in list(data_dict):
        information_dict['id'] = data_dict["id"]
    
    for key in keys:
        try:
            information_dict[key] = data_dict[key]
        except:
            information_dict[key] = None
    # 类型装换
    for key in ["photos","hobbies","temperament",]:
        try:
            information_dict[key] = ";".join(information_dict[key])
        except:pass

    # 将字符串转换为date对象
    information_dict["birthDate"] = datetime.strptime(information_dict["birthDate"], "%Y-%m-%d").date()
    return information_dict

def 提取资产信息(only_key, data_dict):
    '''
    @Time    :   2024/11/21 13:58:39
    @功能    :   None
    例子
    {
        "id": 0,
        "用户唯一标识": "凤欣然_1992-11-10_2024-11-10",
        "类型": "0 表示房产；1 表示车. 如果选择0则车品牌默认将被设置为空；反之 城市和详细地址将被设置为空",
        "是否有贷款":"无贷款",
        "是否在自己名下": "在",
        "城市": "沭阳",
        "详细地址": "xxxx小区x栋xxxx单元xxxx室",
        "车品牌": "奥迪",
        "其他": "沭"
    },
    '''
    def format_data(data, type:int):
        tmp = {"only_key": only_key,
            "asset_type": type,
            "is_me": data['is_me'],
            "is_loan":data['is_loan'],
            "city": "",
            "address": "",
            "brand": "",
            "other": ""}
        if type == 0:
            tmp['city'] = data['city']
            tmp['address'] = data['address']
        else:
            tmp['brand'] = data['brand']
        if "id" in list(data):
            tmp["id"] = data["id"]
        return tmp
    
    asset_house_list = [format_data(data, 0) for data in data_dict['house_info']]
    asset_car_list = [format_data(data, 1) for data in data_dict['cars']]
    return asset_house_list+asset_car_list

def 提取父母兄弟姐妹信息(only_key, data_dict):
    '''
    @Time    :   2024/11/21 16:06:21
    @功能    :   None
    模板
    {
        "id": 0,
        "用户唯一标识": "凤欣然_1992-11-10_2024-11-10",
        "关系": "爸爸",
        "婚姻状况": "已婚",
        "是否健康": "健康",
        "是否退休": "未退休",
        "工作城市":"",
        "月收入": 14636,
        "年收入": 9
    }
    '''
    def 补全字段值(data_dict):
        '''@功能    :   字段值必须具备下面keys的所有值，没有的则置为None'''
        keys = ["relations","maritalStatus","health_status","work_type","monthIncome","yearIncome","work_city"]
        for data in data_dict:
            for key in keys:
                if key in list(data):continue
                data[key] = None
    
    def 重组信息(data_dict):
        family_list = []
        for data in data_dict:
            tmp = {
                "id": None,
                "only_key": only_key,
                "relations": data['relations'],
                "maritalStatus":data['maritalStatus'],
                "health_status": data['health_status'],
                "work_type": data['work_type'],
                "work_city":data['work_city'],
                "monthIncome": data['monthIncome'],
                "yearIncome": data['yearIncome']
            }
            if "id" in list(data):
                tmp["id"] = data["id"]
            family_list.append(tmp)
        return family_list
    补全字段值(data_dict['parents'])
    if "brothers" not in list(data_dict):
        data_dict['brothers'] = []
    补全字段值(data_dict['brothers'])
    family_list = 重组信息(data_dict['parents'])
    family_list += 重组信息(data_dict['brothers'])
    return family_list

def 提取子女信息(only_key, data_dict):
    '''
    @Time    :   2024/11/21 16:14:36
    @功能    :   None
    模板
    {
        "id": 0,
        "用户唯一标识": "凤欣然_1992-11-10_2024-11-10",
        "关系":"",
        "性别": "",
        "年龄": "",
        "是否在身边": "",
        "对方是否出抚养费": "",
        "是否有其他补充": "",
        "照片": "",
        "身高": 166,
        "体重": 80,
        "学历": "博士后",
        "专业": "生物医学工程",
        "学校": "北京大学"
    },
    '''
    children_list = []
    if "childrens" not in list(data_dict):
        return children_list
    for data in data_dict['childrens']:
        tmp = {
            "id": 0,
            "only_key": only_key,
            "relations":data['relations'],
            "sex": data['sex'],
            "age": data['age'],
            "photos": "",
            "children_around": data['children_around'],
            "children_support_payment": data['children_support_payment'],
            "other": data['other'],
            "height": None,
            "weight": None,
            "education": "",
            "major": "",
            "school": ""
        }
        if "id" in list(data):
            tmp["id"] = data["id"]
        children_list.append(tmp)
    return children_list

def GetClientIP(request: Request):
    '''
    @Time    :   2024/11/25 16:05:03
    @功能    :   获得客户端的ip
    '''
    # 尝试从X-Forwarded-For头部获取IP，如果不存在，则尝试X-Real-IP，最后退回到remote address
    ip = request.headers.get("X-Forwarded-For")
    if not ip:
        ip = request.headers.get("X-Real-IP")
    if not ip:
        ip = request.client.host  # 作为最后的手段，可能不是真实的客户端IP
    return ip

def 将table中的数据恢复为前端数据结构(db, table,only_keys):
    '''根据获得的完整的only_key 获得所有的数据，按照表生成字典'''
    # 根据获得的完整的only_key 获得所有的数据，按照表生成字典
    results = information_crud.search_multi_table(db, table,"only_key", only_keys)
    # 每个表内部根据only_key生成字典,最终映射到每个表
    table_result_dict = {}
    for model, value_list in results.items():
        # 获取所有字段名称
        search_results_dicts = [result.to_dict() for result in value_list]
        only_key_dict = {}
        for data_dict in search_results_dicts:
            if data_dict['only_key'] not in list(only_key_dict):
                only_key_dict[data_dict['only_key']] = []
            only_key_dict[data_dict['only_key']].append(data_dict)
        table_result_dict[model.__tablename__] = only_key_dict
    return table_result_dict

def 资产统计(assets):
    '''
    @功能    :   统计资产信息
    '''
    key = "is_loan"
    anytime_buy, asset_counts, asset_loan = None, 0, []
    for data in assets:
        if data[key] == "无": continue
        if data[key] == "随时可以买": 
            anytime_buy = data[key]
            continue
        asset_counts += 1
        if data[key] not in asset_loan:
            asset_loan.append(data[key])

    if len(asset_loan) > 1:     asset_loan = "部分有贷款"
    elif len(asset_loan) == 1:  asset_loan = asset_loan[0]
    else:   asset_loan = anytime_buy
    return asset_counts, asset_loan
    
def 组织前端返回的搜索条件(data_dict, fieldMapping_dict):
    '''
    @Time    :   2024/11/28 13:32:25
    @功能    :   None
    '''
    order_fields, limit, offset = None, None, None
    if "search" in list(data_dict):
        pass

    if "search_fields" in list(data_dict):
        if "sort" in list(data_dict):
            sort = data_dict['sort']
            for key, value in fieldMapping_dict.items():
                if value == sort['field']:
                    sort['field'] = key
                    break
            order_fields = [(sort['field'], sort['sort'])]

        if "field_search" in list(data_dict):
            new_field_search = {}
            for key, value_dict in data_dict['field_search'].items():
                new_key = None
                for web_key, table_key in fieldMapping_dict.items():
                    if value == web_key:
                        new_key = table_key
                        new_field_search[new_key] = {}
                        break
                if "conditions" in list(value_dict):
                    new_field_search[new_key]["operator"] = value_dict["operator"]

    
    if "limit" in list(data_dict):
        limit = data_dict['limit']
    if "offset" in list(data_dict):
        offset = data_dict['offset']
    return offset, limit, order_fields

################################################################################
################################ 数据库操作 ####################################
################################################################################

# 组织更新记录数据
def InsertUpdateRecord(db, data):
    '''
    @Time    :   2024/11/25 11:03:02
    @功能    :   插入新的更新数据库记录
    '''
    try:
        result = update_record_crud.create(db, **data)
    except Exception as e:
        with codecs.open("插入修改记录失败.log", "a", "utf-8") as fa:
            fa.write(f"错误信息:{e}\n{str(data)}\n")
        return None
    return result
################################################################################

app_get = APIRouter()
@app_get.get('/fieldMapping',
        summary='获得mapping信息',
        description='详细描述',
        response_description='响应的描述信息')
async def fieldMapping(db: Session = Depends(get_db)):
    try:
        # 使用CRUD实例
        all_obj_list = fieldmapping_crud.read_all(db)
        field_mapping_dict = {obj.web_field:obj.table_field for obj in all_obj_list}
        return {"status":1,"field_mapping":field_mapping_dict}
    except:
        return {"status":0,"field_mapping":{}}

@app_get.get('/showFields',
        summary='获得mapping信息',
        description='详细描述',
        response_description='响应的描述信息')
async def showFields(db: Session = Depends(get_db)):
    try:
        all_obj_list = show_filed_crud.read_all(db)
        show_fields_list = {}
        for obj in all_obj_list:
            show_fields_list = eval(obj.fields)
        return {"status":1,"show_fields":show_fields_list}
    except:
        return {"status":0,"show_fields":{}}

@app_get.get('/select_options',
        summary='获得mapping信息',
        description='详细描述',
        response_description='响应的描述信息')
async def select_options(db: Session = Depends(get_db)):
    try:
        all_obj_list = select_crud.read_all(db)
        all_select_options_dict = {obj.name:eval(obj.items) for obj in all_obj_list}
        return {"status":1,"select_options":all_select_options_dict}
    except:
        return {"status":0,"select_options":{}}
 
def table数据还原成web数据_asset(table_result_dict, results_dict):
    '''
    @Time    :   2024/11/29 14:19:27
    @功能    :   将table中的数据还原成为web端数据的存储格式，准备返回前端
    '''
    house_keys = ['id', 'is_loan', 'is_me', 'address', 'city']
    car_keys = ['id', 'is_loan', 'brand', 'is_me']
    if "asset" not in list(table_result_dict): return
    for only_key, datas_list in table_result_dict['asset'].items():
        house_info, cars = [], []
        for data_dict in datas_list:
            if data_dict['asset_type'] == 0:
                values_dict = {key:data_dict[key] for key in house_keys}
                house_info.append(values_dict)
            elif data_dict['asset_type'] == 1:
                values_dict = {key:data_dict[key] for key in car_keys}
                cars.append(values_dict)
        results_dict[only_key]["house_info"] = house_info 
        results_dict[only_key]["cars"] = cars 
    pass
def table数据还原成web数据_familys(table_result_dict,results_dict):
    '''
    @Time    :   2024/11/29 14:19:27
    @功能    :   将table中的数据还原成为web端数据的存储格式，准备返回前端
    '''
    for only_key, datas_list in table_result_dict.items():
        parents, brothers = [], []
        for data_dict in datas_list:
            del data_dict['create_time']
            del data_dict['only_key']
            if data_dict['relations'] in ['父亲','母亲']:
                parents.append(data_dict)
            else:
                brothers.append(data_dict)
        results_dict[only_key]["parents"] = parents 
        results_dict[only_key]["brothers"] = brothers 
    pass

def table数据还原成web数据_childrens(only_key, table_result_dict,results_dict):
    '''
    @Time    :   2024/11/29 14:19:27
    @功能    :   将table中的数据还原成为web端数据的存储格式，准备返回前端
    '''
    children_keys = ['id', 'sex', 'age', 'children_around', 'children_support_payment', 'other', 'relations']
    if table_result_dict == {}:
        results_dict[only_key]["childrens"] = childrens 
        return None
    for only_key, datas_list in table_result_dict.items():
        childrens = []
        for data_dict in datas_list:
            value_dict = {key:data_dict[key] for key in children_keys}
            childrens.append(value_dict)
        results_dict[only_key]["childrens"] = childrens 
    return results_dict

################################################################################
################################ 个人信息表操作 #################################
################################################################################
app = APIRouter()
@app.get('/information/',
            summary='根据个人唯一id获得个人信息',
            description='详细描述',
            response_description='响应的描述信息')
async def information_get(name: Optional[str] = Query(None), 
                          db: Session = Depends(get_db)):

    # 判断某个key是否存在
    results = information_crud.multi_field_multi_value_search(db, {"only_key":name})
    only_keys = [res.only_key for res in results]
    # 将关系对象转为dict
    if only_keys == []: return {"status":-1,"datas":[], "msg":"没有该用户相关信息"}

    results_dict = {result.only_key:result.to_dict() for result in results}
    # 每个表内部根据only_key生成字典,最终映射到每个表
    table_result_dict = 将table中的数据恢复为前端数据结构(db, [AssetTable, FamilysTable, ChildrenTable],only_keys)

    # 将每个表中的only_key 数据整合为前端数据
    # 转换个人资产
    table数据还原成web数据_asset(table_result_dict,results_dict)

    # 转换父母兄弟姐妹信息
    table数据还原成web数据_familys(table_result_dict["familys"],results_dict)
    # 转换子女信息
    table数据还原成web数据_childrens(name, table_result_dict["children"],results_dict)
    
    # 将相关信息进行转换
    results_list = []
    for key in results_dict:
        results_dict[key]["birthDate"] = results_dict[key]["birthDate"].strftime('%Y-%m-%d')
        for field in ["hobbies", "temperament"]:
            try:
                results_dict[key][field] = results_dict[key][field].split(";")
            except:
                results_dict[key][field] = []
        results_list.append(results_dict[key])
    
    # 所有数据按照only_key 生成前端相同的数据结构返回给前端
    return {"status":1,"datas":results_list}

@app.post('/information_table',
            summary='根据搜索条件获得所有数据',
            description='详细描述',
            response_description='响应的描述信息')
async def information_get_all(request:Request, db: Session = Depends(get_db)):
    try:
        data_dict = await request.json()
    except:
      {"status":0, "msg":"提交的信息有误","datas":[]}
    fieldmapping_results = fieldmapping_crud.read_all(db)
    field_mapping_dict = {obj.table_field:obj.web_field for obj in fieldmapping_results}
    offset, limit, order_fields = 组织前端返回的搜索条件(data_dict, fieldmapping_results)
        
    print("返回所有数据")
    if data_dict == {}:
        results = information_crud.read_all(db, limit=limit,offset=offset,order_fields=order_fields)
    else:
        # page_size: 需要获取的数据量
        # currentPage: 需要获取第几页数据
        # totalPages: 一共几页数据
        offset = data_dict['page_dict']['currentPage']*data_dict['page_dict']['page_size']
        limit = data_dict['page_dict']['page_size']
        results, total_count = information_crud.search_by_value(db, data_dict["search"], offset=offset,limit=limit)
        pass
    # results = asset_crud.multi_field_multi_value_search(db, search_criteria={"only_key":[key]})
    results_dict = {result.only_key:result.to_dict() for result in results}
    datas = []

    for key in list(results_dict):

        familys_results = familys_crud.multi_field_multi_value_search(db, {"only_key":key})
        familys_results_list = [result.to_dict() for result in familys_results]
        parents_list, brothers_list = [], []
        for family_dict in familys_results_list:
            if family_dict['relations'] in ['父亲','母亲',]:
                parents_list.append({
                    "relations":family_dict['relations'],
                    "health_status":family_dict['health_status'],
                    "year_income":family_dict['year_income'],
                    "work_type":family_dict['work_type'],
                    "maritalStatus":family_dict['maritalStatus']
                    })
            else:
                brothers_list.append({
                    "relations":family_dict['relations'],
                    "health_status":family_dict['health_status'],
                    "year_income":family_dict['year_income'],
                    "work_type":family_dict['work_type'],
                    "maritalStatus":family_dict['maritalStatus']
                    })

        results_dict[key]['parents'] = parents_list
        results_dict[key]['brothers'] = brothers_list


        results_dict[key]['birthDate'] = results_dict[key]['birthDate'].strftime('%Y-%m-%d')
        datas.append(results_dict[key])
    
    new_datas = []
    for index, data in enumerate(datas):
        new_data = {}
        for key in list(field_mapping_dict):
            try:
                new_data[field_mapping_dict[key]] = data[key]
            except: pass
        new_data['子女(个)'] = data['childrens_number']

        new_data['房产(数量)'] = data['houses']
        new_data['房贷款'] = data['house_loan']

        new_data['车(数量)'] = data['cars']
        new_data['车贷款'] = data['car_loan']
        if new_data['性格'] == None: new_data['性格']=""
        new_datas.append(new_data)
        pass
    for i in range(7):
        new_datas += new_datas
    return {"status":1,"datas":new_datas, "msg":"信息获取正常"}
    
@app.post('/information',
            # response_model=Information,
            summary='填写个人信息',
            description='详细描述',
            response_description='响应的描述信息')
async def information_post(request:Request, db: Session = Depends(get_db)):
    try:
        data_dict = await request.json()
    except:
      {"status":0, "msg":"提交的信息有误"}
    only_key = 生成OnlyKey(data_dict)
    information_dict = 提取个人信息(only_key, data_dict)
    information_dict['houses'], information_dict['house_loan'] = 资产统计(data_dict['house_info'])
    information_dict['cars'], information_dict['car_loan'] = 资产统计(data_dict['cars'])

    # 判断某个key是否存在
    results = information_crud.multi_field_multi_value_search(db, {"only_key":rf'{information_dict["name"]}_{information_dict["birthDate"]}'})
    if len(results)!= 0:
        return {"status":-1, "msg":"系统中已经存在该客户的信息，请先确认该客户是否已经填写过个人信息"}
    # 假设表中已经有数据，获取最后一条数据

    try:
        last_user = db.query(InformationTable).order_by(InformationTable.id.desc()).first()
        information_dict["id"] = last_user.id+1
    except:
        information_dict["id"] = 0

    # 提取数据
    asset_information_list = 提取资产信息(only_key, data_dict)
    family_list = 提取父母兄弟姐妹信息(only_key, data_dict)
    children_list = 提取子女信息(only_key, data_dict)  

    # 插入记录
    new_user = information_crud.create(db, **information_dict)
    liabilities_datas = 向table批量插入数据(db, AssetTable, asset_information_list)
    family_datas = 向table批量插入数据(db, FamilysTable, family_list)
    children_datas = 向table批量插入数据(db, ChildrenTable, children_list)

    return {"status":1, "msg":"提交成功"}

@app.put('/information',    
            summary='更新个人信息',
            description='详细描述',
            response_description='响应的描述信息')
async def information_put(request:Request, db: Session = Depends(get_db)):
    # 个人信息，资产，家庭，子女 四个数据库的增 删 改 完成，
    # 记录每一次的修改记录 完成
    def 获取操作数据库的动作和数据(table_data, web_data):
        crud_dict = {"del":[],"update":[],"post":[],}
        if table_data == {}: return crud_dict
        # 新增的数据的id是None值
        crud_dict['post'] = [["", data] for data in web_data if data["id"] == None]
        # list 转 dict，使用id作为下标
        table_data_dict = {data["id"]:data for data in table_data}
        web_data_dict = {data["id"]:data for data in web_data if data["id"] != None}
        # 获得被删除的id列表
        crud_dict['del'] = [[table_data_dict[id],""] for id in list(table_data_dict) if id not in list(web_data_dict)]

        # 获得更新的数据
        for id in list(web_data_dict):
            data = web_data_dict[id]
            # 遍历每个字段进行对比
            for key in list(data):
                if str(data[key]) != str(table_data_dict[id][key]):
                    crud_dict["update"].append([table_data_dict[id], data])
                    break
        return crud_dict

    def 更新个人相关信息并记录更新动作(asset_crud_dict, asset_crud, table_name):
        for data in asset_crud_dict['update']:
            data['create_time'] = datetime.now()
            udpate_result = asset_crud.update_dict(db, data[-1]['id'], data[-1])
            组织更新记录并更新(db, data, table_name, client_ip, udpate_owner,"update")
        for data in asset_crud_dict['del']:
            udpate_result = asset_crud.delete(db, data[0]['id'])
            组织更新记录并更新(db, data, table_name, client_ip, udpate_owner,"del")
        for data in asset_crud_dict['post']:
            data['create_time'] = datetime.now()
            del data[1]["id"]
            udpate_result = asset_crud.create(db, **data[1])
            组织更新记录并更新(db, data, table_name, client_ip, udpate_owner,"post")
    
    def 组织更新记录并更新(db, data, table_name, client_ip, udpate_owner, type):
        
        record_data={
            "only_key":only_key,
            "type":type,
            "table_name":table_name,
            "update_ip":client_ip,
            "update_owner":udpate_owner,
            "old_data":str(data[0]),
            "new_data":str(data[1])
        }
        InsertUpdateRecord(db, record_data)

    try:
        request_dict = await request.json()
    except:
        {"status":0, "msg":"提交更新的数据有错误请仔细核实"}

    client_ip = GetClientIP(request)
    request_dict["user_name"] = "这是一个测试用户名称"
    udpate_owner = "这是一个测试用户名称"
    # 将信息格按照不同的表拆分重组
    only_key = request_dict['only_key']
    # 判断某个key是否存在
    results = information_crud.multi_field_multi_value_search(db, {"only_key":request_dict['only_key']})
    if len(results) != 1:
        return {"status":-1, "msg":"警告: 本条记录已经丢失，将生成新纪录，同时请检查系统安全"}
    
    id = results[0].id
    information_dict = 提取个人信息(only_key, request_dict)
    information_dict['houses'], information_dict['house_loan'] = 资产统计(request_dict['house_info'])
    information_dict['cars'], information_dict['car_loan'] = 资产统计(request_dict['cars'])

    asset_information_list = 提取资产信息(only_key, request_dict)
    
    family_list = 提取父母兄弟姐妹信息(only_key, request_dict)
    children_list = 提取子女信息(only_key, request_dict)

    results = information_crud.multi_field_multi_value_search(db, {"only_key":request_dict['only_key']})
    # 模糊搜索获得所有的 only_key
    only_keys = [res.only_key for res in results]
    # 将关系对象转为dict
    results_dict = {result.only_key:result.to_dict() for result in results}

    # 每个表内部根据only_key生成字典,最终映射到每个表
    table_result_dict = table_result_dict = 将table中的数据恢复为前端数据结构(db, [AssetTable, FamilysTable, ChildrenTable], only_keys)

    # 对比个人基本信息表
    for key in list(information_dict):
        if key == "id": continue
        if str(information_dict[key]) != str(results_dict[only_key][key]):
            print("需要更新")
            information_dict["id"] = id
            # 更新数据库，并且记录本条修改
            udpate_result = information_crud.update_dict(db, id, information_dict)
            组织更新记录并更新(db, [results_dict[only_key], information_dict], "information", client_ip, udpate_owner,"update")
            break

    # 对比个人资产表
    asset_crud_dict = 获取操作数据库的动作和数据(table_result_dict['asset'][only_key], asset_information_list)
    更新个人相关信息并记录更新动作(asset_crud_dict, asset_crud, 'asset')

    # 对比家庭信息表
    familys_crud_dict = 获取操作数据库的动作和数据(table_result_dict['familys'][only_key], family_list)
    更新个人相关信息并记录更新动作(familys_crud_dict, familys_crud, 'familys')

    # 对比子女表
    if table_result_dict['children'] != {}:
        children_crud_dict = 获取操作数据库的动作和数据(table_result_dict['children'][only_key], children_list)
        更新个人相关信息并记录更新动作(children_crud_dict, children_crud, 'children')

    return {"status":1, "msg":"提交更新成功"}

@app.delete('/information/{id}',
            summary='删除个人信息',
            description='详细描述',
            response_description='响应的描述信息')
async def information_del(db: Session = Depends(get_db)):
    return {"information":""}
################################################################################

################################################################################
################################ 个人要求表操作 #################################
################################################################################
app_request = APIRouter()


def GetRangeFunc(sex, value, min_value, max_value):
    '''
    @Time    :   2024/12/03 17:42:10
    @功能    :   None
    '''
    min, max = -1, -1
    if sex == "女":
        min = value - min_value
        max = value + max_value
    else:
        min = value - max_value
        max = value + min_value
    return {"min":min, "max":max}

def HeightRange(sex):
    '''
    @Time    :   2024/12/03 17:46:35
    @功能    :   None
    '''
    min, max = -1, -1
    if sex == "女":
        min, max = 170, 185
    else:
        min, max = 155, 170
    return {"min":min, "max":max}
def WeighttRange(sex):
    '''
    @Time    :   2024/12/03 17:46:35
    @功能    :   None
    '''
    min, max = -1, -1
    if sex == "女":
        min, max = 60, 80
    else:
        min, max = 45, 70
    return {"min":min, "max":max}

def InitRequestInfo(information_dict, name):
    '''
    @Time    :   2024/12/06 12:22:26
    @功能    :   没有创建要求的用户的初始要求信息
    '''
    initialValues={
        "only_key":name,
        "house_info": { 
            "assets_number": {"min":None, "max":None}, 
            "is_loan": ['无要求'], 
            "city": ["沭阳"], 
            "is_me":["在"] 
        },
        "car":{ 
            "assets_number": {"min":None, "max":None}, 
            "is_loan": ['无要求'], 
            "brand": ["无要求"], 
            "is_me":["在"]
        },
        "sex":"男",
        "parents":[
            {
                "relations":"父亲",
                "health_status":["健康"],
                "maritalStatus":["已婚"],
                "monthIncome_range":{"min":None, "max":None},
                "yearIncome_range":{"min":None, "max":None},
                "work_type":['无要求']
            },
            {
                "relations":"母亲",
                "health_status":["健康"],
                "maritalStatus":["已婚"],
                "monthIncome_range":{"min":None, "max":None},
                "yearIncome_range":{"min":None, "max":None},
                "work_type":['无要求']
            }
        ],
        "brothers":[
            # {
            #     "relations":"哥哥",
            #     "health_status":["健康"],
            #     "maritalStatus":["已婚"],
            #     "monthIncome_range":{"min":3000, "max":5000},
            #     "yearIncome_range":{"min":3, "max":6},
            #     "work_type":['无要求']
            # },
            # {
            #     "relations":"姐姐",
            #     "health_status":["健康"],
            #     "maritalStatus":["已婚"],
            #     "monthIncome_range":{"min":5000, "max":9000},
            #     "yearIncome_range":{"min":6, "max":12},
            #     "work_type":['无要求']
            # },
        ],
        "appearance":["无要求"],
        "maritalStatus":["无要求"],
        "childrens_number":0,
        "childrens":[
            # {"sex":["无要求"],
            # "age_range":{"min":0, "max":3},
            # "children_around":["无要求"], #是否在身边
            # "children_support_payment":["不出"],#对方是否出抚养费
            # "other":None
            # },
            # {"sex":["无要求"],
            # "age_range":{"min":0, "max":3},
            # "children_around":["无要求"], #是否在身边
            # "children_support_payment":["无要求"],#对方是否出抚养费
            # "other":None    
            # },
        ],
        "photos_public":["无要求"],
        "temperament":["无要求"],
        "workType":["无要求"],
        "workCity":["无要求"],
        "workUnit":["无要求"],
        "school":None,
        "major":["无要求"],
        "hobbies":["无要求"],
        "drinking":["无要求"],
        "smorking":["无要求"],
        "Hope_settle_city":["无要求"],
        "academic_qualifications":["无要求"],
        "age_range":GetRangeFunc(information_dict['sex'], information_dict['age'], 1, 3),
        "monthIncome_range":GetRangeFunc(information_dict['sex'], information_dict['monthIncome'], 1000, 3000),
        "yearIncome_range":GetRangeFunc(information_dict['sex'], information_dict['yearIncome'], 1, 3),
        "bank_deposit_range":{"min":0, "max":200},
        "height_range":HeightRange(information_dict['sex']),
        "weight_range":WeighttRange(information_dict['sex'])
    }
    if information_dict['sex'] == "男":
        initialValues["sex"] = "女"
    return initialValues

@app_request.get('/request',
            summary='根据个人唯一id获得个人要求信息',
            description='详细描述',
            response_description='响应的描述信息')
async def request_get(name: Optional[str] = Query(None), 
                          db: Session = Depends(get_db)):
    # 判断某个key是否存在
   
    name = "张长啸_1996-04-08_2024-12-03"
    results = request_crud.multi_field_multi_value_search(db, {"only_key":name})
    # results = []
    if results == []:
        information_results = information_crud.multi_field_multi_value_search(db, {"only_key":name})
        information_dict_list = [result.to_dict() for result in information_results]
        initialValues = InitRequestInfo(information_dict_list[0], name)
        return {"status":1,"initialValues":initialValues, "url_type":"post", "msg":"没有找到个人要求基本信息,则更新个人信息自动生成一部分要求信息"}
    else:
        table_result_dict = 将table中的数据恢复为前端数据结构(db, [RequestTable, RequestAssetTable,RequestFamilysTable, ReeuestChildrenTable], name)
        for key, value_dict in table_result_dict.items():
            table_result_dict[key] = value_dict[name]

        # 将表中所有的范围和下拉列表回复
        request_table_keys = ["id","only_key","sex","birthDate_range","age_range","photos_public","Hope_settle_city","temperament",
        "appearance","maritalStatus","height_range","weight_range","drinking","smorking","monthIncome_range",
        "yearIncome_range","bank_deposit_range","workType","workCity","workUnit","academic_qualifications",
        "major","school","educational_supplements","childrens_number","hobbies","create_time","other"]
        # 恢复列表字段
        list_keys = ["birthDate_range","photos_public","temperament","appearance","maritalStatus","drinking","smorking","workType","workCity","workUnit","academic_qualifications","major","school","hobbies","Hope_settle_city"]
        range_keys = ["age_range","height_range","weight_range","monthIncome_range","yearIncome_range","bank_deposit_range"]
        
        initialValues = {}
        datas = table_result_dict['request'][0]
        for key in request_table_keys:
            request_value = datas[key]
            if key in list_keys:
                try:
                    request_value = request_value.split(";;")
                except:pass
            elif key in range_keys:
                try:
                    tmp_list = request_value.split(";;")
                    request_value = {"min":int(tmp_list[0]), "max":int(tmp_list[1])}
                except:
                    request_value = {"min":None, "max":None}
            initialValues[key] = request_value

        # 资产要求
        request_asset_keys = ["id","asset_type","assets_number","is_loan","is_me","city","address","brand","other"]
        asset_list_keys = ["is_loan", "is_me"]
        asset_range_keys = ['assets_number']
        for datas in table_result_dict['request_asset']:
            for key in request_asset_keys:
                request_value = datas[key]
                if key in asset_list_keys:
                    try:
                        request_value = request_value.split(";;")
                    except:pass
                elif key in asset_range_keys:
                    try:
                        tmp_list = request_value.split(";;")
                        request_value = {"min":int(tmp_list[0]), "max":int(tmp_list[1])}
                    except:
                        request_value = {"min":None, "max":None}
                datas[key] = request_value
            if datas["asset_type"] == 0:
                initialValues["house_info"] = datas
            elif datas["asset_type"] == 1:
                initialValues["car"] = datas

        # 家庭信息
        request_familys_keys = ["id","relations","maritalStatus","health_status","work_type","work_city","monthIncome_range","yearIncome_range"]
        familys_list_keys = ["maritalStatus", "health_status","work_type"]
        familys_range_keys = ["monthIncome_range","yearIncome_range"]
        initialValues["parents"], initialValues["brothers"] = [], []
        for datas in table_result_dict['request_familys']:
            for key in request_familys_keys:
                request_value = datas[key]
                if key in familys_list_keys:
                    try:
                        request_value = request_value.split(";;")
                    except:pass
                elif key in familys_range_keys:
                    try:
                        tmp_list = request_value.split(";;")
                        request_value = {"min":int(tmp_list[0]), "max":int(tmp_list[1])}
                    except:
                        request_value = {"min":None, "max":None}
                datas[key] = request_value
            if datas["relations"] in ["父亲","母亲"]:
                initialValues["parents"].append(datas)
            else:
                initialValues["brothers"].append(datas)

        # 子女信息
        request_children_keys = ["id","sex","age_range","relations","photos_public","children_around","children_support_payment","other"]
        children_list_keys = ["sex", "children_around", "children_support_payment"]
        children_range_keys = ["age_range"]
        initialValues["childrens"] = []
        for datas in table_result_dict['request_children']:
            for key in request_children_keys:
                request_value = datas[key]
                if key in children_list_keys:
                    try:
                        request_value = request_value.split(";;")
                    except:pass
                elif key in children_range_keys:
                    try:
                        tmp_list = request_value.split(";;")
                        request_value = {"min":int(tmp_list[0]), "max":int(tmp_list[1])}
                    except:
                        request_value = {"min":None, "max":None}
                datas[key] = request_value
            initialValues["childrens"].append(datas)
        return {"status":1,"initialValues":initialValues, "url_type":"put", "msg":"找到个人要求基本信息,修改后将会以更新的方式"}

@app_request.post('/request_table',
            summary='根据搜索条件获得所有数据',
            description='详细描述',
            response_description='响应的描述信息')
async def request_get_all(request:Request, db: Session = Depends(get_db)):
    try:
        data_dict = await request.json()
    except:
      {"status":0, "msg":"提交的信息有误","datas":[]}
    fieldmapping_results = fieldmapping_crud.read_all(db)
    field_mapping_dict = {obj.table_field:obj.web_field for obj in fieldmapping_results}
    
    offset, limit, order_fields = 组织前端返回的搜索条件(data_dict, fieldmapping_results)
        
    print("返回所有数据")
    if data_dict == {}:
        results = information_crud.read_all(db, limit=limit,offset=offset,order_fields=order_fields)
    else:
        # page_size: 需要获取的数据量
        # currentPage: 需要获取第几页数据
        # totalPages: 一共几页数据
        offset = data_dict['page_dict']['currentPage']*data_dict['page_dict']['page_size']
        limit = data_dict['page_dict']['page_size']
        results, total_count = information_crud.search_by_value(db, data_dict["search"], offset=offset,limit=limit)
        pass
    # results = asset_crud.multi_field_multi_value_search(db, search_criteria={"only_key":[key]})
    results_dict = {result.only_key:result.to_dict() for result in results}
    datas = []

    for key in list(results_dict):

        familys_results = familys_crud.multi_field_multi_value_search(db, {"only_key":key})
        familys_results_list = [result.to_dict() for result in familys_results]
        parents_list, brothers_list = [], []
        for family_dict in familys_results_list:
            if family_dict['relations'] in ['父亲','母亲',]:
                parents_list.append({
                    "relations":family_dict['relations'],
                    "health_status":family_dict['health_status'],
                    "year_income":family_dict['year_income'],
                    "work_type":family_dict['work_type'],
                    "maritalStatus":family_dict['maritalStatus']
                    })
            else:
                brothers_list.append({
                    "relations":family_dict['relations'],
                    "health_status":family_dict['health_status'],
                    "year_income":family_dict['year_income'],
                    "work_type":family_dict['work_type'],
                    "maritalStatus":family_dict['maritalStatus']
                    })

        results_dict[key]['parents'] = parents_list
        results_dict[key]['brothers'] = brothers_list


        results_dict[key]['birthDate'] = results_dict[key]['birthDate'].strftime('%Y-%m-%d')
        datas.append(results_dict[key])
    
    new_datas = []
    for index, data in enumerate(datas):
        new_data = {}
        for key in list(field_mapping_dict):
            try:
                new_data[field_mapping_dict[key]] = data[key]
            except: pass
        new_data['子女(个)'] = data['childrens_number']

        new_data['房产(数量)'] = data['houses']
        new_data['房贷款'] = data['house_loan']

        new_data['车(数量)'] = data['cars']
        new_data['车贷款'] = data['car_loan']
        if new_data['性格'] == None: new_data['性格']=""
        new_datas.append(new_data)
        pass
    for i in range(7):
        new_datas += new_datas
    return {"status":1,"datas":new_datas, "msg":"信息获取正常"}
    
@app_request.post('/add',
            # response_model=Information,
            summary='填写个人要求信息',
            description='详细描述',
            response_description='响应的描述信息')
async def add(request:Request, db: Session = Depends(get_db)):
    try:
        data_dict = await request.json()
    except:
      {"status":0, "msg":"提交的信息有误"}
    request_table_keys = ["only_key","sex","birthDate_range","age_range","photos_public","Hope_settle_city","temperament",
    "appearance","maritalStatus","height_range","weight_range","drinking","smorking","monthIncome_range",
    "yearIncome_range","bank_deposit_range","workType","workCity","workUnit","academic_qualifications",
    "major","school","educational_supplements","childrens_number","hobbies","create_time","other"]
    # 房产 是否有贷款 是否在自己名下 所在城市
    # 车子 是否有贷款 是否在自己名下 品牌
    data_dict["birthDate_range"] = {
        "min":根据年龄计算出生日期(data_dict['age_range']['min']),
        "max":根据年龄计算出生日期(data_dict['age_range']['max'])
    }
    data_dict['create_time'] = datetime.now()
    data_dict['educational_supplements'] = None
    data_dict['other'] = None
    request_table_dict, not_find_keys = {}, []
    for key in request_table_keys:
        try:
            request_table_dict[key] = data_dict[key]
        except:
            not_find_keys.append(key)
    for key, value_dict in request_table_dict.items():
        if key in ["birthDate_range","age_range","height_range","weight_range","monthIncome_range","yearIncome_range","bank_deposit_range"]:
            try:
                value_dict = f"{value_dict['min']};;{value_dict['max']}"
            except: pass
        if key in ["photos_public","temperament","appearance","maritalStatus","drinking","smorking","workType","workCity","workUnit","academic_qualifications","major","school","hobbies","Hope_settle_city"]:
            try:
                value_dict = ";;".join(value_dict)
            except: pass
        request_table_dict[key] = value_dict

    only_key = request_table_dict['only_key']
    
    # 资产要求
    request_asset_keys = ["assets_number","is_loan","is_me","city","address","brand","other"]
    assert_list = []
    for key in ["house_info", "car"]:
        tmp = { "only_key":only_key, "create_time":datetime.now()}
        if key == "house_info": tmp['asset_type'] = 0
        elif key == "car":      tmp['asset_type'] = 1
        for key1 in request_asset_keys:
            try:
                tmp[key1] = data_dict[key][key1]
            except:
                tmp[key1] = None
                continue
            if key1 == "assets_number":
                tmp['assets_number'] = f"{data_dict[key][key1]['min']};;{data_dict[key][key1]['max']}"
            if key1 in  ["is_loan", "is_me"]:
                tmp[key1] = ";;".join(tmp[key1])
        assert_list.append(tmp)

        pass
    # 家庭信息
    request_familys_keys = ["relations","maritalStatus","health_status","work_type","work_city","monthIncome_range","yearIncome_range"]
    request_familys_list = []
    for key0 in ["parents", "brothers"]:
        for value_dict in data_dict[key0]:
            tmp = { "only_key":only_key, "create_time":datetime.now()}
            for key in request_familys_keys:
                try:
                    tmp[key] = value_dict[key]
                except:
                    tmp[key] = None 
                    continue
                if key in ["monthIncome_range","yearIncome_range"]:
                    tmp[key] = f"{value_dict[key]['min']};;{value_dict[key]['max']}"
                if key in ["maritalStatus", "health_status","work_type"]:
                    tmp[key] = ";;".join(tmp[key])
            request_familys_list.append(tmp)

    # 子女信息
    request_children_keys = ["sex","age_range","relations","photos_public","children_around","children_support_payment","other"]
    request_children_list = []
    for key0 in ["childrens"]:
        for value_dict in data_dict[key0]:
            tmp = { "only_key":only_key, "create_time":datetime.now()}
            for key in request_children_keys:
                try:tmp[key] = value_dict[key]
                except:
                    tmp[key] = None 
                    continue
                if key in ["age_range"]:
                    tmp[key] = f"{value_dict[key]['min']};;{value_dict[key]['max']}"
                if key in ["sex", "children_around", "children_support_payment"]:
                    tmp[key] = ";;".join(tmp[key])
            request_children_list.append(tmp)

    # 插入记录
    new_user = request_crud.create(db, **request_table_dict)
    liabilities_datas = 向table批量插入数据(db, RequestAssetTable, assert_list)
    family_datas = 向table批量插入数据(db, RequestFamilysTable, request_familys_list)
    children_datas = 向table批量插入数据(db, ReeuestChildrenTable, request_children_list)

    return {"status":1, "msg":"提交成功"}

@app_request.put('/put',    
            summary='更新个人要求信息',
            description='详细描述',
            response_description='响应的描述信息')
async def request_put(request:Request, db: Session = Depends(get_db)):
    # 个人信息，资产，家庭，子女 四个数据库的增 删 改 完成，
    try:
        data_dict = await request.json()
    except:
      {"status":0, "msg":"提交的信息有误"}
    request_table_keys = ["id","only_key","sex","age_range","photos_public","Hope_settle_city","temperament",
    "appearance","maritalStatus","height_range","weight_range","drinking","smorking","monthIncome_range",
    "yearIncome_range","bank_deposit_range","workType","workCity","workUnit","academic_qualifications",
    "major","school","educational_supplements","childrens_number","hobbies","other",
    # "birthDate_range","create_time"
    ]
    # 房产 是否有贷款 是否在自己名下 所在城市
    # 车子 是否有贷款 是否在自己名下 品牌
    # data_dict["birthDate_range"] = {
    #     "min":根据年龄计算出生日期(data_dict['age_range']['min']),
    #     "max":根据年龄计算出生日期(data_dict['age_range']['max'])
    # }
    data_dict['create_time'] = datetime.now()
    data_dict['educational_supplements'] = None
    data_dict['other'] = None
    request_table_dict, not_find_keys = {}, []
    for key in request_table_keys:
        try:
            request_table_dict[key] = data_dict[key]
        except:
            not_find_keys.append(key)
    for key, value_dict in request_table_dict.items():
        if key in ["birthDate_range","age_range","height_range","weight_range","monthIncome_range","yearIncome_range","bank_deposit_range"]:
            try:
                value_dict = f"{value_dict['min']};;{value_dict['max']}"
            except: pass
        if key in ["photos_public","temperament","appearance","maritalStatus","drinking","smorking","workType","workCity","workUnit","academic_qualifications","major","school","hobbies","Hope_settle_city"]:
            try:
                value_dict = ";;".join(value_dict)
            except: pass
        request_table_dict[key] = value_dict

    only_key = request_table_dict['only_key']
    
    # 资产要求
    request_asset_keys = ["id","assets_number","is_loan","is_me","city","address","brand","other"]
    assert_list = []
    for key in ["house_info", "car"]:
        # tmp = { "only_key":only_key, "create_time":datetime.now()}
        tmp = { "only_key":only_key}
        if key == "house_info": tmp['asset_type'] = 0
        elif key == "car":      tmp['asset_type'] = 1
        for key1 in request_asset_keys:
            try:
                tmp[key1] = data_dict[key][key1]
            except:
                tmp[key1] = None
                continue
            if key1 == "assets_number":
                tmp['assets_number'] = f"{data_dict[key][key1]['min']};;{data_dict[key][key1]['max']}"
            if key1 in  ["is_loan", "is_me"]:
                tmp[key1] = ";;".join(tmp[key1])
        assert_list.append(tmp)
        pass
    # 家庭信息
    request_familys_keys = ["id","relations","maritalStatus","health_status","work_type","work_city","monthIncome_range","yearIncome_range"]
    request_familys_list = []
    for key0 in ["parents", "brothers"]:
        data_dict_list = data_dict[key0]
        for value_dict in data_dict_list:
            # tmp = { "only_key":only_key, "create_time":datetime.now()}
            tmp = { "only_key":only_key}
            for key in request_familys_keys:
                try:
                    tmp[key] = value_dict[key]
                except:
                    tmp[key] = None 
                    continue
                if key in ["monthIncome_range","yearIncome_range"]:
                    tmp[key] = f"{value_dict[key]['min']};;{value_dict[key]['max']}"
                if key in ["maritalStatus", "health_status","work_type"]:
                    tmp[key] = ";;".join(tmp[key])
            request_familys_list.append(tmp)

    # 子女信息
    request_children_keys = ["id","sex","age_range","relations","photos_public","children_around","children_support_payment","other"]
    request_children_list = []
    for key0 in ["childrens"]:
        for value_dict in data_dict[key0]:
            # tmp = { "only_key":only_key, "create_time":datetime.now()}
            tmp = { "only_key":only_key}
            for key in request_children_keys:
                try:tmp[key] = value_dict[key]
                except:
                    tmp[key] = None 
                    continue
                if key in ["age_range"]:
                    tmp[key] = f"{value_dict[key]['min']};;{value_dict[key]['max']}"
                if key in ["sex", "children_around", "children_support_payment"]:
                    tmp[key] = ";;".join(tmp[key])
            request_children_list.append(tmp)

    # # 判断数据是否修改
    # res = request_crud.multi_field_multi_value_search(db, search_criteria=request_table_dict, search_mode="eq")
    # if len(res) != 0:
    #     print("所有字段沒有更改")
    # else:
    #     print("需要修改")
    # for asset_data in assert_list:
    #     res = request_asset_crud.multi_field_multi_value_search(db, search_criteria=asset_data, search_mode="eq")
    #     if len(res) != 0:
    #         print("所有字段沒有更改")
    #     else:
    #         print("需要修改")
    # for asset_data in request_familys_list:
    #     res = request_familys_crud.multi_field_multi_value_search(db, search_criteria=asset_data, search_mode="eq")
    #     if len(res) != 0:
    #         print("所有字段沒有更改")
    #     else:
    #         print("需要修改")

    # for asset_data in request_children_list:
    #     res = request_children_crud.multi_field_multi_value_search(db, search_criteria=asset_data, search_mode="eq")
    #     if len(res) != 0:
    #         print("所有字段沒有更改")
    #     else:
    #         print("需要修改")

    table_result_dict = 将table中的数据恢复为前端数据结构(db, [RequestAssetTable, RequestFamilysTable, ReeuestChildrenTable], [only_key])
    client_ip = GetClientIP(request)
    udpate_owner = "这是一个测试用户名称"
   
    # 记录每一次的修改记录 完成
    def 获取操作数据库的动作和数据(table_data, web_data):
        crud_dict = {"del":[],"update":[],"post":[],}
        if table_data == {}: return crud_dict
        # 新增的数据的id是None值
        crud_dict['post'] = [["", data] for data in web_data if data["id"] == None]
        # list 转 dict，使用id作为下标
        table_data_dict = {data["id"]:data for data in table_data}
        web_data_dict = {data["id"]:data for data in web_data if data["id"] != None}
        # 获得被删除的id列表
        crud_dict['del'] = [[table_data_dict[id],""] for id in list(table_data_dict) if id not in list(web_data_dict)]

        # 获得更新的数据
        for id in list(web_data_dict):
            data = web_data_dict[id]
            # 遍历每个字段进行对比
            for key in list(data):
                if str(data[key]) != str(table_data_dict[id][key]):
                    crud_dict["update"].append([table_data_dict[id], data])
                    break
        return crud_dict

    def 更新个人相关信息并记录更新动作(asset_crud_dict, asset_crud, table_name):
        for data in asset_crud_dict['update']:
            data['create_time'] = datetime.now()
            udpate_result = asset_crud.update_dict(db, data[-1]['id'], data[-1])
            组织更新记录并更新(db, data, table_name, client_ip, udpate_owner,"update")
        for data in asset_crud_dict['del']:
            udpate_result = asset_crud.delete(db, data[0]['id'])
            组织更新记录并更新(db, data, table_name, client_ip, udpate_owner,"del")
        for data in asset_crud_dict['post']:
            data['create_time'] = datetime.now()
            del data[1]["id"]
            udpate_result = asset_crud.create(db, **data[1])
            组织更新记录并更新(db, data, table_name, client_ip, udpate_owner,"post")
    
    def 组织更新记录并更新(db, data, table_name, client_ip, udpate_owner, type):
        record_data={
            "only_key":only_key,
            "type":type,
            "table_name":table_name,
            "update_ip":client_ip,
            "update_owner":udpate_owner,
            "old_data":str(data[0]),
            "new_data":str(data[1])
        }
        InsertUpdateRecord(db, record_data)
        
    def 表更新提示(asset_crud_dict, msg):
        '''
        @Time    :   2024/12/06 15:01:41
        @功能    :   None
        '''
        for key in ["del","update","post",]:
            if asset_crud_dict[key] != []:
                msg_list.append(f"{msg} 已经更新完成")
                break
        pass
    
    results = request_crud.multi_field_multi_value_search(db, {"only_key":only_key})
    # 将关系对象转为dict
    results_dict = {result.only_key:result.to_dict() for result in results}

    # 对比个人基本信息表
    # information_dict 前端传回的结果
    # results_dict 数据库查询的结果
    msg_list = []
    for key in list(request_table_dict): 
        if key == "id": continue
        if str(request_table_dict[key]) != str(results_dict[only_key][key]):
            print("需要更新")
            id = results_dict[only_key]["id"]
            # 更新数据库，并且记录本条修改
            request_table_dict['create_time'] = datetime.now()
            udpate_result = request_crud.update_dict(db, id, request_table_dict)
            组织更新记录并更新(db, [results_dict[only_key], request_table_dict], "request", client_ip, udpate_owner,"update")
            msg = f"个人要求表 已经更新完成"
            if msg not in msg_list:
                msg_list.append(msg)

    # 对比个人资产表
    asset_crud_dict = 获取操作数据库的动作和数据(table_result_dict['request_asset'][only_key], assert_list)
    更新个人相关信息并记录更新动作(asset_crud_dict, request_asset_crud, 'request_asset')
    表更新提示(asset_crud_dict, "资产要求表")

    # 对比家庭信息表
    familys_crud_dict = 获取操作数据库的动作和数据(table_result_dict['request_familys'][only_key], request_familys_list)
    更新个人相关信息并记录更新动作(familys_crud_dict, request_familys_crud, 'request_familys')
    表更新提示(familys_crud_dict, "家庭要求表")

    # 对比子女表
    if table_result_dict['request_children'] != {}:
        children_crud_dict = 获取操作数据库的动作和数据(table_result_dict['request_children'][only_key], request_children_list)
        更新个人相关信息并记录更新动作(children_crud_dict, request_children_crud, 'request_children')
        表更新提示(children_crud_dict, "子女要求表")

    return {"status":1, "msgs":msg_list}

@app_request.delete('/request/{id}',
            summary='删除个人要求信息',
            description='详细描述',
            response_description='响应的描述信息')
async def request_del(db: Session = Depends(get_db)):
    return {"information":""}

################################################################################

##################################### 以下内容可以放到一个独立main.py中运行 #################################################
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# from fastapi_test import app as app_router  #独立为main.py 需要导入写好的api

# 启用 CORS
origins = ["http://localhost:5173"]
# 创建 FastAPI 应用实例
main_api = FastAPI()
main_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 允许所有域名访问
    allow_credentials=True, # 允许携带cookies
    allow_methods=["*"], # 允许所有方法
    allow_headers=["*"], # 允许所有头
)

main_api.include_router(app,tags=["个人信息表"])
main_api.include_router(app_get, prefix="/get",tags=["只支持get的表"])
main_api.include_router(app_request, prefix="/request",tags=["个人要求表"])

def Main():
    '''
    @Time    :   2024/08/12 15:19:49
    @功能    :   None
    fastapi 命令解析：
    # uvicorn 执行的py文件名称:FastAPI()创建的名称 --host ip地址 --port 端口号
    实例如下：
    # uvicorn fastapi_test:app --host 10.233.202.137 --port 7767
    '''
    uvicorn.run("fastapi_test:main_api", host="10.233.202.137", port=7767, reload=True)
    pass

if __name__ == '__main__':
    Main()
    pass


