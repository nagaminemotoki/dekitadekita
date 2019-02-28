%rebase("base.tpl")

<p>{{user_name_tpl}}さん、こんにちは</p>

<table border="1"></table>
    %for item in task_list_tpl:
    <tr>
        <td>{{item["id"]}}</td>
        <td>{{item["task"]}}</td>
        <td><a href="/edit/{{item['id']}}">編集</a></td>
        <td><a href="/del/{{item['id']}}">削除</a></td>
    </tr>
    %end
</table>

<a href="/add">リストの追加はこちら</a>

<a href="/logout">ログアウト</a>