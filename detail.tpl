<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>できた！</title>
    <link rel="stylesheet" href="../static/css/style.css">
</head>

<body>
    <div class="container">
        <p>{{tpl_item['dekita']}}</p>
        <p>{{tpl_item['time']}}</p>
        <a href="/del/{{tpl_item['id']}}">削除</a>
    </div>
</body>

</html>