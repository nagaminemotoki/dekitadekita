%rebase("base.tpl",title="あなたの「できた」を教えて")

<div class="container">

    <div class="kuma_relative">
        <img class="kuma" src="static/img/marekuma.png">
        <img class="logo" src="static/img/dekita_logo.png">
    </div>

    <p></p>
    <p class="intro">できたできた〜そんなあなたに。できたできた〜できたできた〜そんなあなたに。
        できたできた〜できたできた〜そんなあなたに。できたできた〜できたできた〜そんなあなた
    </p>
    <p></p>
    <h2 class="message">あなたも<br>「できたできた」はじめてみる？</h2>
    <!--  -->
    <form action="/login" method="post">
        <input type="text" name="name" placeholder="名前" class="input"><br>
        <input type="password" name="password" placeholder="パスワード" class="input"><br>
        <input type="submit" name="login" value="ログイン" class="btn">
    </form>
    <br>

    <div class="regist">
        <div class="profile-solid icon"></div>
        <a href="/regist" class="orange">新規登録する方はこちら</a>
    </div>
</div>