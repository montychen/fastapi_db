from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas


def get_books_by_name(db: Session, bookname: str):  # 根据书名查询，支持模糊查询
    return db.query(models.Book).filter(models.Book.bookname.like(f"%{bookname}%")).all()


def delete_book_by_Id(db: Session, bookId: int):  # 根据书的`ID`删除
    db_book = db.query(models.Book).filter(
        models.Book.id == bookId).one_or_none()
    if db_book is None:
        return None
    db.delete(db_book)
    db.commit()
    return True


def create_book(db: Session, book: schemas.BookBase):  # 增加书籍信息
    curBook = models.Book(
        bookname=book.bookname,
        prices=book.prices,
        datetime=datetime.now(),
    )
    db.add(curBook)   # 数据库表Books的id字段的值，自动生成
    db.commit()
    db.refresh(curBook)
    return curBook


def update_book_by_id(db: Session, bookId: int, book: schemas.BookBase):  # 根据书的`ID`修改书籍信息
    db_book = db.query(models.Book).filter(
        models.Book.id == bookId).one_or_none()
    if db_book is None:
        return None

    # 利用了Python的vars函数，可以将一个对象的所有属性以字典的方式列举。
    for var, value in vars(book).items():
        # python的函数setattr()，用于设置属性值，这里是更新书籍的信息
        setattr(db_book, var, value) if value else None
    
    db.commit()
    db.refresh(db_book)
    return db_book
