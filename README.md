# run 
我们是用 from . import XXX
相对路径的方式导入当前文件夹下的其它文件, 在这种情况下, 必须将当前目录切换到 fastapi_db 的**上一级目录**来运行
```bash
uvicorn fastapi_db.main:app --reload 
```
