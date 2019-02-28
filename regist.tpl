%rebase("base.tpl",title="登録しよう！")

<div class="container">
    <form action="/regist" method="post">
        <input type="text" name="name" placeholder="名前"><br>
        <input type="password" name="password" placeholder="パスワード"><br>
        <input type="submit" name="regist" value="新規登録" class="btn">
    </form>
    %if user_check_tpl != 0:
    <p>その名前は登録できないよ！</p>
    %end
</div>