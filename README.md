# Flask-Todo-list 
這是一個具有待辦事項功能的網站，並有基本的會員機制，登入後可新增、查看、修改、刪除個人待辦事項

<img src="https://github.com/ts00193189/flask-todo-list/blob/main/image/home.PNG">

## 安裝環境
```
pip install -r requirements.txt
```

## 執行App
Bash：
```
export FLASK_APP=main.py
flask run
```

CMD：
```
set FLASK_APP=main.py
flask run
```
執行後可連線至 http://127.0.0.1:5000/todo/ 查看


## 執行測試
```
flask test
```

## 登入
登入帳號，登入後才可使用待辦事項

<img src="https://github.com/ts00193189/flask-todo-list/blob/main/image/login.PNG">

## 註冊
註冊帳號，註冊網站會員，密碼長度需為8~20字

<img src="https://github.com/ts00193189/flask-todo-list/blob/main/image/register.PNG">
