#クライアントもサーバもすべてじぶんのPCで実行（テスト環境）・ローカルホスト

import os
#routeとrun（実行）とtemplateとTEMPLATE_PATHの機能をインポート
from bottle import route, run, template, TEMPLATE_PATH, redirect, request, error, response, static_file, datetime
import sqlite3
import secrets #パスワードなど知られたくない情報をランダムでつくる機能
secret_cookie = secrets.token_hex()

#app.pyのあるところと、bottleフォルダのパスを合体（？）
TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname("__file__"), "../dekita0228_02")))

#---------------------------------------------------------------------------

@route('/')
def top():
    return template("top.tpl")

#---------------------------------------------------------------------------

@route('/regist', method=["GET"])
def regist_get():
    user_id = request.get_cookie("user_id", secret=secret_cookie) #nameからuser_idに変更（nameなら重複する可能性）
    
    name = request.POST.getunicode("name")
    
    if user_id is None:
        conn = sqlite3.connect('dekita.db')
        c = conn.cursor()
        c.execute("select count(name) from user where name = ?",(name,))
        user_check = c.fetchone()[0]
        # print(user_check)
        return template('regist', user_check_tpl = user_check)
    else:
        return redirect('/dekita')

@route('/regist', method=["POST"])
def regist_post():
    name = request.POST.getunicode("name")
    password = request.POST.getunicode("password")

    conn = sqlite3.connect('dekita.db')
    c = conn.cursor()

    c.execute("select count(name) from user where name = ?",(name,))
    user_check = c.fetchone()[0]
    # print(user_check)

    if user_check == 0:
        c.execute("insert into user values(null, ?, ?)",(name, password))
        conn.commit()
        conn.close()
    # return redirect('/login')
        return template('login')
    else:
        conn.close()
        return template('regist', user_check_tpl = user_check)
        
#---------------------------------------------------------------------------

@route("/login", method = ["GET"])
def login_get():
    user_id = request.get_cookie("user_id", secret=secret_cookie) #secret_cookieは暗号化の文字列
    if user_id is None:
        return template("top")
    else:
        return redirect("/dekita")

@route("/login", method = ["POST"])
def login_post():
    name = request.POST.getunicode("name")
    password = request.POST.getunicode("password")
    conn = sqlite3.connect('dekita.db')
    c = conn.cursor()
    c.execute("select id from user where name = ? and pass = ?;", (name,password))
    user_id = c.fetchone()
    conn.close()
    if user_id is not None:
        # print(user_id)
        user_id = user_id[0]
        response.set_cookie("user_id", user_id, secret=secret_cookie) #Webブラウザ上にcookieを置く
        return redirect('/dekita')
    else:
        return template("top")

#---------------------------------------------------------------------------

@route('/dekita')
def dekita():
    #>>追加
    user_id = request.get_cookie("user_id", secret=secret_cookie)
    #<<
    conn = sqlite3.connect('dekita.db')
    c = conn.cursor()
    c.execute('select name from user where id = ?', (user_id,))
    user_name = c.fetchone()[0]
    # print(user_name)
    c.execute("select count(del_flag) from dekita where user_id = ? and del_flag = 0", (user_id,))
    sum = c.fetchone()[0]
    print(sum)
    today_check = datetime.now().strftime('%Y/%m/%d')
    today_check = today_check + "%"
    # print(today_check)
    c.execute("select count(del_flag) from dekita where user_id = ? and del_flag = 0 and time like ?", (user_id,today_check))
    sum_today = c.fetchone()[0]
    print(sum_today)

    if sum_today == 0 and sum != 0:
        time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        c.execute('insert into dekita values(null,?,?,?,?);', (user_id,"ログインできた！",time, 0))
        conn.commit()

    if sum == 0:
        time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        c.execute('insert into dekita values(null,?,?,?,?);', (user_id,"登録できた！",time, 0))
        conn.commit()

    c.execute("select id, dekita, time from dekita where user_id = ? and del_flag = 0 order by id desc", (user_id,))
    # if not dekita == None:
    #空のdekita_listに変数を追加
    dekita_list = []
    #dekitaテーブルから取得してきたデータを追加
    #fetchall()と書いているのでテーブルの中身すべて
    youbis = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for row in c.fetchall():
        ymd = row[2][0:10] #年月日
        msm = row[2][11:20]#分秒ミリ（？）秒
        youbi_number = datetime.strptime(ymd,'%Y/%m/%d')
        youbi = youbis[youbi_number.weekday()]
        dekita_list.append({'id':row[0], "dekita":row[1], "ymd":ymd, "msm":msm, "youbi":youbi})
        c.close()
    if sum == 0:
        return template("dekita", user_name_tpl = user_name, dekita_list_tpl = dekita_list, sum_tpl = 1, sum_today_tpl = 1)
    else:
        return template("dekita", user_name_tpl = user_name, dekita_list_tpl = dekita_list, sum_tpl = sum, sum_today_tpl = sum_today)

#---------------------------------------------------------------------------

@route("/logout")
def logout():
    response.set_cookie("user_id", None, secret=secret_cookie)
    return redirect("/")

#---------------------------------------------------------------------------

# add.tplの表示
@route('/add', method = ["GET"])
def add_get():
    return template("dekita")

@route('/add', method = ["POST"])
def add_post():
    #追加
    user_id = request.get_cookie("user_id", secret=secret_cookie)
    #フォームから入力されたデータを取得
    dekita = request.POST.getunicode('dekita')
    #データベースと接続---
    conn = sqlite3.connect('dekita.db')
    c = conn.cursor()
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    c.execute('insert into dekita values(null,?,?,?,?);', (user_id,dekita,time, 0))
    #データベースを保存する
    conn.commit()
    conn.close()
    return redirect('/dekita') #入力後'/'に飛ぶ

#---------------------------------------------------------------------------

@route('/del/<id:int>')
def del_dekita(id):
    conn = sqlite3.connect('dekita.db')
    c = conn.cursor()
    # c.execute("delete from dekita where id = ?", (id,))
    c.execute("update dekita set del_flag = 1 where id = ?;", (id,))
    conn.commit()
    conn.close()
    return redirect('/dekita')

#---------------------------------------------------------------------------

@route('/detail/<id:int>')
def detail(id):
    conn = sqlite3.connect('dekita.db')
    c = conn.cursor()
    c.execute("select dekita, time from dekita where id = ?;", (id,))
    dekita_one = c.fetchone()
    conn.close()
    if dekita_one is not None:
        dekita = dekita_one[0] #("チョコレート")から"チョコレート"にするため
        time = dekita_one[1]
    else:
        return "アイテムがありません"
    item = {"id":id, "dekita":dekita, "time":time}
    return template("detail", tpl_item = item)

# @route('/detail', method=["POST"])
# def detail_dekita():
#     item_id = request.POST.getunicode('dekita_id')
#     item_id = int(item_id)
#     dekita = request.POST.getunicode('dekita')
#     conn = sqlite3.connect('dekita.db')
#     c = conn.cursor()
#     c.execute("update dekita set dekita = ? where id = ?;", (dekita, item_id))
#     conn.commit()
#     conn.close()
#     return redirect('/dekita')

#---------------------------------------------------------------------------

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root="static")

#---------------------------------------------------------------------------

@error(404)
def notfound(code):
    return template("404")

run(port = "8080", reloader = True) #Pythonファイルを実行, データを読み直す・IPアドレスは住所、portは部屋番号


