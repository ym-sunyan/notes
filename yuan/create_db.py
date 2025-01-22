
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
    children_sex:str            #性别
    children_age: int           #年龄
    children_around:str         #是否在身边
    children_support_payment:str#对方是否出抚养费
    children_other: Optional[str]=None  #其他补充信息
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
    # photosPublic: Optional[str] = None  #照片是否公开
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
    __table_args__ = (
        {'info': {'doc': '个人基本信息.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': '个人资产情况.'}},  # 表级别的文档说明
    )
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    liabilities_type = Column( Integer,index=True, doc="资产类型。0 表示房产；1 表示车. 如果选择0则车品牌默认将被设置为空；反之 城市和详细地址将被设置为空",comment="资产类型。0 表示房产；1 表示车. 如果选择0则车品牌默认将被设置为空；反之 城市和详细地址将被设置为空")
    is_loan = Column( String,index=True, doc="是否有贷款",comment="是否有贷款")
    is_me = Column( String,index=True, doc="是否在我名下",comment="是否在我名下")
    liabilities_city = Column( String,index=True, doc="房子所在城市",comment="房子所在城市")
    address = Column( String,index=True, doc="房子详细地址",comment="房子详细地址")
    car_brand = Column( String,index=True, doc="汽车品牌",comment="汽车品牌")
    other = Column( Text,index=True, doc="其他的一些说明，或者强调一些事情",comment="其他的一些说明，或者强调一些事情")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class FamilysTable(Base):
    # 父母兄弟表
    __tablename__ = "familys"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = (
        {'info': {'doc': '个人家庭情况，父母兄弟姐妹.'}},  # 表级别的文档说明
    )
    id = Column(Integer, primary_key=True ,index=True, autoincrement=True, doc="id",comment="id")
    only_key = Column(String ,index=True, doc="数据库中唯一的key，基本在所有表中都有使用",comment="数据库中唯一的key，基本在所有表中都有使用")
    relations = Column( String,index=True, doc="关系",comment="关系")
    maritalStatus = Column( String,index=True, doc="婚姻状况",comment="婚姻状况")
    health_status = Column( String,index=True, doc="健康状况",comment="健康状况")
    work_type = Column( String,index=True, doc="工作类型",comment="工作类型")
    work_city = Column( String,index=True, doc="工作城市",comment="工作城市")
    month_income = Column( Integer,index=True, doc="月薪，单位人民币元",comment="月薪，单位人民币元")
    year_income = Column( Integer,index=True, doc="年薪，单位人民币万元",comment="年薪，单位人民币万元")
    create_time = Column(DateTime ,index=True, default=datetime.now(),doc="生成时间",comment="生成时间")
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ChildrenTable(Base):
    # 子女表
    __tablename__ = "children"
    # 使用__table_args__添加表的文档说明信息
    __table_args__ = (
        {'info': {'doc': '个人子女情况.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': '男女匹配情况.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': '对某个客户的评论.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': '匹配成功后，红娘的追踪情况.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': '下拉列表项，固定的字段不需要每次关系.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': '将在web表格中显示的字段.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': 'web表格中的字段和数据库的映射关系.'}},  # 表级别的文档说明
    )
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
    __table_args__ = (
        {'info': {'doc': '对数据库表中所有的修改都被记录再次，该表数据不允许删除.'}},  # 表级别的文档说明
    )
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

# 创建每一张表的CRUD实例
information_crud = CRUDGeneric(InformationTable)    # 个人基本信息表CRUD实例
asset_crud = CRUDGeneric(AssetTable)        # 资产信息表CRUD实例
familys_crud = CRUDGeneric(FamilysTable)    # 父母兄弟表CRUD实例
children_crud = CRUDGeneric(ChildrenTable)  # 子女表CRUD实例
match_crud = CRUDGeneric(MatchingSituationTable)    # 男女匹配情况CRUD实例
select_crud = CRUDGeneric(SelectOptions)    # 项目中使用的下拉列表项CRUD实例
show_filed_crud = CRUDGeneric(ShowFields)   # web显示的字段CRUD实例
fieldmapping_crud = CRUDGeneric(FieldMapping)   # web表格中的字段和数据库的映射关系CRUD实例
redress_crud = CRUDGeneric(RedressTrackTable)   # 红娘追踪记录CRUD实例
evaluation_crud = CRUDGeneric(EvaluationTable)  # 评价表CRUD实例
update_record_crud = CRUDGeneric(UpdateRecordTabel) # 对数据库的所有修改的记录CRUD实例

select_options = {
    "work_type_arr":{
        "list":["务农","公务员","教师","医生","护士","独立创业者","科技工作者","金融工作者"],
        "desc":"工作类型"
    },
    "marital_status":{
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
    "parents_work_status":{
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
    "health_status":{
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
    # "是否公开": "photosPublic",
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
    for index, data_dict in enumerate(datas):
        data_dict["id"] = last_id+index+1
        datas[index] = data_dict
    new_datas = table_crud.create_many(db, datas)
    return new_datas

# 创建表格
Base.metadata.create_all(bind=engine)
# # 使用CRUD实例
# db = SessionLocal()
# 向table批量插入数据(db, SelectOptions, select_options_list)
# 向table批量插入数据(db, ShowFields, show_fields_list)
# 向table批量插入数据(db, FieldMapping, fieldMapping_list)


