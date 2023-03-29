"""
数据库中表对应的模型文件：models.py
"""
from sqlalchemy import Column, Integer, String  # type: ignore
# 导入在database.py文件创建的基类Base. 如果提示导入警告，可以在当前文件夹下新建__init__.py空文件，这样语法检查器会认为这是一个包，可以被导入而不会出现警告。
from .databases import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    bookname = Column(String(100), unique=True)
    prices = Column(Integer)
