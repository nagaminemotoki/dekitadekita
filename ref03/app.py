import os
import sqlite3
# 課題2の答えはここ(一番右) 時間を取得するためにimportする
from bottle import route, run, debug, template, request, static_file, error, redirect, response , datetime , get, TEMPLATE_PATH
# secrets.token_hex([nbytes=None])
# 十六進数のランダムなテキスト文字列を返します。文字列は nbytes のランダムなバイトを持ち、各バイトは二つの十六進数に変換されます。nbytes が None の場合や与えられなかった場合は妥当なデフォルト値が使われます。
import secrets

TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname("__file__"), "../ref03")))

secret_cookie = secrets.token_hex()
print(secret_cookie)

@route('/')
def index():
    print("ここでもsecret_cookie:" + secret_cookie)
    return template('index')


# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@route('/register',method=["GET", "POST"])
def register():
    #  登録ページを表示させる
    if request.method == "GET":
        # ログインしてないからクッキーがセットされてない
        name = request.get_cookie("user_id" , secret="secret_cookie")
        if name is None:

            return template("register")
        else:
            # クッキーセットされてたら、get_cookieできるから/bbsに飛ぶ
            return redirect("/bbs")
    # ここからPOSTの処理
    else:
        # 登録ページで登録ボタンを押した時に走る処理
        
        name = request.POST.getunicode("name")
        password = request.POST.getunicode("password")

        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # 課題4の答えはここ
        c.execute("insert into user values(null,?,?,'no_img.png')", (name,password))
        conn.commit()
        conn.close()
        return redirect('/login')


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@route("/login", method=["GET", "POST"])
def login():
    if request.method == "GET":
        user_id = request.get_cookie("user_id", secret="secret_cookie")
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

        # DBから取得してきたuser_id、ここの時点ではタプル型
        print(type(user_id))

        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if user_id is not None:
            user_id = user_id[0]

            # 上記でインデックス0の値を再代入しているので、ここではint型
            print(type(user_id))

            # クッキー(ブラウザ側に)にnameを記憶させる
            # これで誰が今ログインしているのか判定できる
            response.set_cookie("user_id", user_id, secret='secret_cookie')
            return redirect("/bbs")
        else:
            # ログイン失敗すると、ログイン画面に戻す
            return template("login")

@route("/logout")
def logout():
    # ログアウトはクッキーに None を設定してあげるだけ
    response.set_cookie("user_id", None, secret='secret_cookie')
    return redirect("/login") # ログアウト後はログインページにリダイレクトさせる


@route('/bbs')
def bbs():
    # クッキーからuser_idを取得
    user_id = request.get_cookie("user_id", secret="secret_cookie")
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
    # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
    c.execute("select name,prof_img from user where id = ?", (user_id,))
    # fetchoneはタプル型
    user_info = c.fetchone()
    # user_infoの中身を確認                                         
    # user_infoタプルの1番目を取ってきたい
    print(user_info)
# user_info[1] = space.jpg
    # 課題1の答えはここ del_flagが0のものだけ表示する
    # 課題2の答えはここ 保存されているtimeも表示する
    c.execute("select id,comment,time from bbs where userid = ? and del_flag = 0 order by id", (user_id,))
    comment_list = []
    for row in c.fetchall():
        comment_list.append({"id": row[0], "comment": row[1], "time":row[2]})

    c.close()
    return template('bbs' , user_info = user_info , comment_list = comment_list)



@route('/add', method=["POST"])
def add():
        # クッキーから user_id を取得
        user_id = request.get_cookie("user_id", secret="secret_cookie")
        # 課題2の答えはここ 現在時刻を取得
        time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        # POSTアクセスならDBに登録する
        # フォームから入力されたアイテム名の取得(Python2ならrequest.POST.getunicodeを使う)
        comment = request.POST.getunicode("comment")
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        # 現在の最大ID取得(fetchoneの戻り値はタプル)

        # 課題1の答えはここ null,?,?,0の0はdel_flagのデフォルト値
        # 課題2の答えはここ timeを新たにinsert
        c.execute("insert into bbs values(null,?,?,0,?)", (user_id, comment,time))
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


# /del/100 -> item_id = 100
# /del/50 -> item_id = 50
# /del/one -> HTTPError 404 文字列にするとエラーが出る
# /del/stacafe -> HTTPError 404
# /del/koza -> HTTPError 404
@route("/del/<id:int>"  ,method='POST')
def del_item(id):
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # 指定されたitem_idを元にDBデータを削除せずにdel_flagを1にして一覧からは表示しないようにする

    # 課題1の答えはここ del_flagを1にupdateする
    c.execute("update bbs set del_flag = 1 where id=?", (id,))
    conn.commit()
    conn.close()
    # 処理終了後に一覧画面に戻す
    return redirect("/bbs")

#課題4の答えはここ
@route('/upload', method='POST')
def do_upload():
    # bbs.tplのinputタグ name="upload" をgetしてくる
    upload = request.files.get('upload')
    # upload = request.files.get('upload', '')
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'png,jpg,jpeg形式のファイルを選択してください'
        # パスを取ってくる、下のdef get_save_path():
        # imgフォルダに画像を保存する必要あり。パスをつなごう。関数作ろう。
    save_path = get_save_path()
# imgファイルをstatic/imgフォルダに保存
    upload.save(save_path)
    # ファイル名が取れることを確認、あとで使うよ
    print(upload.filename)

    # アップロードしたユーザのIDを取得
    user_id = request.get_cookie("user_id", secret="secret_cookie")
    conn = sqlite3.connect('service.db')
    c = conn.cursor()
    # update文 
#  (upload.filename) ここで使うよ
    c.execute("update user set prof_img = ? where id=?", (upload.filename,user_id))
    conn.commit()
    conn.close()

    return redirect ('/bbs')

def get_save_path():
    path_dir = "./static/img/"
    return path_dir

# ここまでファイルアップロード、調べてコピペした

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return '404だよ!URL間違ってない！？'



@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(port="8089" ,debug=True, reloader=True)
