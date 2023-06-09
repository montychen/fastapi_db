# 系统要求
- python >= 3.10 
```bash
pip install fastapi
pip install uvicorn[standard]
```
# 开发环境 run 
我们是用 `from . import XXX` 相对路径的方式导入当前文件夹下的其它文件, 在这种情况下, 必须将当前目录切换到 fastapi_db 的**上一级目录**来运行
```bash
uvicorn fastapi_db.main:app --reload 
```

# 生产环境部署 nginx + gunicor + uvicorn
- `gunicorn` 推荐的 worker 数量是系统的 cpu * 2 + 1，不过如果在 docker 或者 k8s 环境中，就要 适当调整了
- nginx 默认配置文件 `nginx.conf` 路径
  - **`nginx -t`** 该命令会输出nginx的配置文件的路径和验证结果
  - mac m1后续， nginx默认配置文件地址是 `/opt/homebrew/etc/nginx/nginx.conf`
  - linux 默认配置文件地址是 `/etc/nginx/nginx.conf`
   


```bash
brew install nginx
brew install gunicorn
```

## 生产环境 run
> 提示： 在终端运行下面的命令， 必须将当前目录切换到 fastapi_db 的**上一级目录**来运行

### 启动 gunicorn
```bash
# 同时会自动启动 uvicorn
# gunicorn.py配置的监听端口是 8000
gunicorn fastapi_db.main:app -c ./fastapi_db/deploy/gunicorn.py
```
访问 [http://127.0.0.1:8000/docs]( http://127.0.0.1:8000/docs) 验证运行正常

### 启动 ningx
一、把自定义配置文件`deploy/nginx.conf`链接到nginx默认配置文件所在的地址,  **ln要使用完整路径**

```bash
#linux    $(pwd)  获得当前目录
sudo ln -s $(pwd)/fastapi_db/deploy/nginx.conf  /etc/nginx/nginx.conf

#mac
ln -s $(pwd)/fastapi_db/deploy/nginx.conf /opt/homebrew/etc/nginx/nginx.conf 
```
二、测试配置文件是否正确，并运行nginx
```bash
nginx -t      
nginx         
```
deploy/nginx.conf 配置的监听端口是 80 访问 [ http://localhost/app/docs](http://localhost/app/docs) 验证nginx运行正常

### 停止 ningx 
这种方法相对于温和一些，需要进程完成当前工作后再停止服务
```bash
nginx -s quit
```

无论进程是否在工作，都直接立即停止进程
```bash
nginx -s stop
```

