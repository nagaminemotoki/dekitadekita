import os
import sqlite3
import secrets
from bottle import route, run, debug, template, TEMPLATE_PATH, request, static_file, error, redirect, response

from datetime import datetime

import sys
import tkinter as tk
import tkinter.messagebox as tkm
root = tk.Tk()
root.attributes('-topmost', True) #ポップアップを最前面に飛ばす
root.withdraw() #tkウインドウを最小化する

secret_cookie = secrets.token_hex()

TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname("__file__"), "../exercise_bbs11")))

@route('/')
def index():
    return template('index')

# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@route('/register',method=["GET", "POST"])
def register():
    if request.method == "GET":
        name = request.get_cookie("name" , secret=secret_cookie)
        if name is None:
            return template("register")
        else:
            return redirect("/bbs")
    # ここからPOSTの処理
    else:
        name = request.POST.getunicode("name")
        password = request.POST.getunicode("password")

        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into user values(null,?,?)", (name,password))
        conn.commit()
        conn.close()
        return redirect('/login')


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@route("/login", method=["GET", "POST"])
def login():
    if request.method == "GET":
        user_id = request.get_cookie("user_id", secret=secret_cookie)
        if user_id is None:
            return template("login")
        else:
            return redirect("/bbs")
    else:
        # ブラウザから送られてきたデータを受け取る
        name = request.POST.getunicode("name")
        password = request.POST.getunicode("password")

        # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
        # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("select id from user where name = ? and password = ?", (name, password) )
        user_id = c.fetchone()
        conn.close()

        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if user_id is not None:
            user_id = user_id[0]
            # クッキー(ブラウザ側に)にnameを記憶させる
            # これで誰が今ログインしているのか判定できる
            response.set_cookie("user_id", user_id, secret=secret_cookie)
            #secret_cookie
            # response.set_cookie("user_id", user_id, secret='startupcafekoza')
            return redirect("/bbs")
        else:
            # ログイン失敗すると、ログイン画面に戻す
            return template("login")

@route("/logout")
def logout():
    # ログアウトはクッキーに None を設定してあげるだけ
    response.set_cookie("user_id", None, secret=secret_cookie)
    return redirect("/login") # ログアウト後はログインページにリダイレクトさせる


@route('/bbs')
def bbs():
    # クッキーからuser_idを取得
    user_id = request.get_cookie("user_id", secret=secret_cookie)
    # print(user_id)
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
    # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
    c.execute("select name from user where id = ?", (user_id,))
    # fetchoneはタプル型
    user_name = c.fetchone()[0]
    c.execute("select id,comment,time,del_flg from bbs where userid = ? order by id", (user_id,))
    comment_list = []
    for row in c.fetchall():
        comment_list.append({"id": row[0], "comment": row[1], "time": row[2], "del_flag": row[3]})
        
    c.close()
    return template('bbs' , user_name = user_name , comment_list = comment_list)

print(datetime.now())

@route('/add', method=["POST"])
def add():
        # クッキーから user_id を取得
        user_id = request.get_cookie("user_id", secret=secret_cookie)
        # POSTアクセスならDBに登録する
        # フォームから入力されたアイテム名の取得(Python2ならrequest.POST.getunicodeを使う)
        comment = request.POST.getunicode("comment")
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        time = datetime.now()
        del_flg = 0
        # DBにデータを追加する
        # c.execute("insert into bbs values(null,?,?)", (user_id, comment))
        c.execute("insert into bbs values(null,?,?,?,?)", (user_id, comment, time, del_flg))
        conn.commit()
        conn.close()
        return redirect('/bbs')


@route('/edit/<id:int>')
def edit(id):
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("select comment from bbs where id = ?", (id,) )
    comment = c.fetchone()
    conn.close()

    if comment is not None:
        # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
        comment = comment[0]
        # "りんご" ○   ("りんご",) ☓
        # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
    else:
        return "アイテムがありません" # 指定したIDの name がなければときの対処

    item = { "id":id, "comment":comment }

    return template("edit", comment=item)


# /add ではPOSTを使ったので /edit ではあえてGETを使う
@route("/edit")
def update_item():
    # ブラウザから送られてきたデータを取得
    item_id = request.GET.getunicode("item_id") # id
    item_id = int(item_id)# ブラウザから送られてきたのは文字列なので整数に変換する
    comment = request.GET.getunicode("comment") # 編集されたテキストを取得する

    # 既にあるデータベースのデータを送られてきたデータに更新
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    c.execute("update bbs set comment = ? where id = ?",(comment,item_id))
    conn.commit()
    conn.close()

    # アイテム一覧へリダイレクトさせる
    return redirect("/bbs")

#----------------------------------------------------------------------------

@route('/del' ,method=["POST"])
def del_task():
    # メッセージボックス（はい・いいえ） 
    # ret = messagebox.askyesno('確認', '本当に削除しますか？')
    ret = tkm.askyesno('確認', '本当に削除しますか？')
    if ret == True:
        id = request.POST.getunicode("comment_id")
        id = int(id)
        conn = sqlite3.connect("service.db")
        c = conn.cursor()
    # c.execute("delete from bbs where id = ?" ,(id,))
        c.execute("update bbs set del_flg = 1 where id = ?;", (id,))
        conn.commit()
        c.close()
        # root.update()
        return redirect("/bbs")
        # sys.exit()
    else:
        # sys.exit()
        # root.update()
        return redirect('/bbs')

#----------------------------------------------------------------------------

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return '404だよ!URL間違ってない！？'

#----------------------------------------------------------------------------

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(port="8081")
