#クライアントもサーバもすべてじぶんのPCで実行（テスト環境）・ローカルホスト

import os
#routeとrun（実行）とtemplateとTEMPLATE_PATHの機能をインポート
from bottle import route, run, template, TEMPLATE_PATH, redirect, request, error, response, static_file
import sqlite3
import secrets #パスワードなど知られたくない情報をランダムでつくる機能
secret_cookie = secrets.token_hex()
# print(secret_cookie)

#app.pyのあるところと、bottleフォルダのパスを合体（？）
TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname("__file__"), "../bottle")))

@route('/')
def top():
    return "ここはトップページだよ！！"

@route('/index')
def index():
    return "Hello World"

@route('/user/<name>')
def user(name):
    return name

@route('/hello/<text>')
def hello(text):
    return text + "さん、こんにちは！"

@route('/temptest')
def temptest():
    name = "スタコザ"
    age = 20
    address = "沖縄県沖縄市中央1-7-8"
    return template('index', name_tpl = name, age_tpl = age, address_tpl = address)

#---------------------------------------------------------------------------

@route('/dbtest')
def dbtest():
    #データベースに接続
    conn = sqlite3.connect('test0212.db')
    #カーソルオブジェクトをつくる・SQL文を使うためのコマンド
    c = conn.cursor()
    c.execute('select name, age, address from users where id = 1;')
    #fetchoneは1行のみとれる・usersのid=1のみだからfetchoneでOK・指定したものの範囲でfetchallもある
    user_info = c.fetchone()
    #データベース接続終了
    c.close()
    #user_infoの中身を確認
    print(user_info)
    return template('dbtest', user_info_tpl = user_info)

#---------------------------------------------------------------------------

#add.tplの表示
@route('/add', method = ["GET"])
def add_get():
    return template('add.tpl')

@route('/add', method = ["POST"])
def add_post():
    #追加
    user_id = request.get_cookie("user_id", secret=secret_cookie)
    #フォームから入力されたデータを取得
    task = request.POST.getunicode('task')
    #データベースと接続---
    conn = sqlite3.connect('test0212.db')
    c = conn.cursor()
    c.execute('insert into task values(null,?,?);', (task,user_id))
    #データベースを保存する
    conn.commit()
    conn.close()
    return redirect('/list') #入力後'/'に飛ぶ

#---------------------------------------------------------------------------

@route('/list')
def list():
    #>>追加
    user_id = request.get_cookie("user_id", secret=secret_cookie)
    # print(user_id)
    #<<
    conn = sqlite3.connect('test0212.db')
    c = conn.cursor()
    # c.execute('select id, task from task where id = ?', (user_id,))
    c.execute('select name from user where id = ?', (user_id,))
    user_name = c.fetchone()[0]
    c.execute("select id, task from task where user_id = ?", (user_id,))
    #空のtask_listに変数を追加
    task_list = []
    #taskテーブルから取得してきたデータを追加
    #fetchall()と書いているのでテーブルの中身すべて
    for row in c.fetchall():
        task_list.append({'id':row[0], "task":row[1]})
        # print(row)
    c.close()
    # print(task_list)
    return template('list.tpl', user_name_tpl = user_name, task_list_tpl = task_list)

#---------------------------------------------------------------------------

@route('/edit/<id:int>')
def edit(id):
    conn = sqlite3.connect('test0212.db')
    c = conn.cursor()
    c.execute("select task from task where id = ?;", (id,))
    task = c.fetchone()
    conn.close()
    # print(task)
    if task is not None:
        # print(task)
        # print(task[0])
        task = task[0] #("チョコレート")から"チョコレート"にするため
    else:
        return "アイテムがありません"
    edit_item = {"id":id, "task":task}
    return template("edit", tpl_item = edit_item)

@route('/edit', method=["POST"])
def update_task():
    item_id = request.POST.getunicode('task_id')
    item_id = int(item_id)
    task = request.POST.getunicode('task')
    conn = sqlite3.connect('test0212.db')
    c = conn.cursor()
    c.execute("update task set task = ? where id = ?;", (task, item_id))
    conn.commit()
    conn.close()
    return redirect('/list')

#---------------------------------------------------------------------------

@route('/del/<id:int>')
def del_task(id):
    conn = sqlite3.connect('test0212.db')
    c = conn.cursor()
    c.execute("delete from task where id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/list')

#---------------------------------------------------------------------------

@route('/regist', method=["GET"])
def regist_get():
    user_id = request.get_cookie("user_id", secret=secret_cookie) #nameからuser_idに変更（nameなら重複する可能性）
    if user_id is None:
        return template('regist')
    else:
        return redirect('/list')

@route('/regist', method=["POST"])
def regist_post():
    name = request.POST.getunicode("name")
    password = request.POST.getunicode("password")

    conn = sqlite3.connect('test0212.db')
    c = conn.cursor()
    c.execute("insert into user values(null, ?, ?)",(name, password))
    conn.commit()
    conn.close()
    return redirect('/login')

#---------------------------------------------------------------------------

@route("/login", method = ["GET"])
def login_get():
    user_id = request.get_cookie("user_id", secret=secret_cookie) #secret_cookieは暗号化の文字列
    if user_id is None:
        return template("login.tpl")
    else:
        return redirect("/list")        

@route("/login", method = ["POST"])
def login_post():
    name = request.POST.getunicode("name")
    password = request.POST.getunicode("password")
    conn = sqlite3.connect('test0212.db')
    c = conn.cursor()
    c.execute("select id from user where name = ? and pass = ?;", (name,password))
    user_id = c.fetchone()
    conn.close()
    if user_id is not None:
        print(user_id)
        user_id = user_id[0]gjjgifdudfihihtin
        response.set_cookie("user_id", user_id, secret=secret_cookie) #Webブラウザ上にcookieを置く
        return redirect('/list')
    else:
        return template("login")

#---------------------------------------------------------------------------

@route("/logout")
def logout():
    response.set_cookie("user_id", None, secret=secret_cookie)
    return redirect("/login")

#---------------------------------------------------------------------------

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root="static")

#---------------------------------------------------------------------------

@error(404)
def notfound(code):
    return "404エラーだよん"

run(port = "8080", reloader = True) #Pythonファイルを実行, データを読み直す・IPアドレスは住所、portは部屋番号


