%rebase("base.tpl",title="掲示板 | 月木でわかる HTML5 &amp; CSS3")

<div>
  <img src="static/img/photo_01.png">
  <p>{{user_name}}さん こんにちは</p><br>

  <form action="/add" method="post">
    投稿者：{{user_name}}<br>
    内容：<textarea name="comment" cols="30" rows="5"></textarea><br>
    <input type="submit" name="save" value="送信">
  </form>
% for item in comment_list:
% if item["del_flag"] != 1: 
  <div class="bbs_content">
    <p>{{item["comment"]}}</p>
    <p>{{item["time"]}}</p>
    <a href="/edit/{{item['id']}}">編集</a>
    <form action="/del" method="post">
      <input type="hidden" name="comment_id" value="{{item['id']}}">
      <input type="submit" name="delete" value="削除する">
    </form><br><br>
  </div>
% end
% end
</div>

<div>
  <a href="/logout">ログアウト</a>
</div>