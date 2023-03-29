"""
数据库表所对应的架构文件: schemas.py;
models.py中是与表严格对应的, 而schemas则可以根据表模型来定制适合不同场景的类。
"""
from typing import Union
from pydantic import BaseModel


# 建立一个去掉id的类，用来新建数据时使用
class BooksBase(BaseModel):
    bookname: str
    prices: Union[int, None] = None


class Books(BooksBase):
    id: Union[int, None] = None

    class Config:  # 这是pydantic的配置，将orm_mode设为True，告诉pydantic，这是可以直接映射为对象关系模型的类
        orm_mode = True
