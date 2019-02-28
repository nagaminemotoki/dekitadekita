%rebase("base.tpl",title="ログインしよう！")

<div class="container">
    <form action="/login" method="post">
        <input type="text" name="name" placeholder="名前"><br>
        <input type="password" name="password" placeholder="パスワード"><br>
        <input type="submit" name="login" value="ログイン" class="btn">
    </form>
</div>