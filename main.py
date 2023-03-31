"""
我们是用 from . import XXX
相对路径的方式导入当前文件夹下的其它文件, 在这种情况下, 必须将当前目录切换到 fastapi_db 的上一级目录来运行

uvicorn fastapi_db.main:app --reload 
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from . import crud, schemas, models
from .databases import SessionLocal, engine

# 根据模板文件创建对应的数据库表，如果表已经存在，不会再次重建
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():  # 设定数据库连接
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.Book])  # 查询书籍
def get_hospital_nums(bookname: str, db: Session = Depends(get_db)):
    db_books = crud.get_books_by_name(db, bookname=bookname)
    if not db_books:
        raise HTTPException(status_code=400, detail="当前书籍名称未查询到相匹配的书籍。")
    return db_books


@app.post("/deleteBook/{bookid}")  # 删除书籍
def delete_book(bookid: int, db: Session = Depends(get_db)):
    return crud.delete_book_by_Id(db, bookId=bookid)


@app.post("/updateBook/{bookid}", response_model=schemas.Book)  # 修改书籍
def update_book(bookid: int, book: schemas.BookBase, db: Session = Depends(get_db)):
    return crud.update_book_by_id(db, bookId=bookid, book=book)


@app.post("/books/", response_model=schemas.Book)  # 新增书籍
def create_book(book: schemas.BookBase, db: Session = Depends(get_db)):
    db_book = crud.get_books_by_name(db, bookname=book.bookname)
    if db_book:
        raise HTTPException(status_code=400, detail="该书籍已经存在。")
    return crud.create_book(db=db, book=book)
