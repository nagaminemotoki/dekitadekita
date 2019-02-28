%rebase("base.tpl")

<form action = "/add" method = "POST">
    <!-- sizeはフォームの文字数サイズ・maxlengthは入力できる最大文字数 -->
    <input type = "text" size = "100" maxlength = "100" name = "task">
    <input type = "submit" name = "save" value = "送信">
</form>