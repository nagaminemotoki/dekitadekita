%rebase("base.tpl",title="掲示板 | 月木でわかる HTML5 &amp; CSS3")

<div>

<p>{{user_info[0]}}さん こんにちは</p><br>
<!-- 課題4の答えはここ -->
<!-- user_info[1]  id と紐づいている -->
<img src="static/img/{{user_info[1]}}" alt="" class="prof_img">
<p>画像変更</p>
<form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="upload"></br>
        <input type="submit" value="画像アップロード"></br>
</form>

  <form action="/add" method="post">
    投稿者：{{user_info[0]}}<br>
    内容：<textarea name="comment" cols="30" rows="5"></textarea><br>
    <input type="submit" name="save" value="送信">
  </form>


    %for item in comment_list:
  <div class="bbs_content">
    <p>{{item["comment"]}}</p>
    <p>投稿時間:{{item["time"]}}</p>
      <a href="/edit/{{item['id']}}">編集</a>
      <!-- 課題3の答えはここ -->
      <a class="delete" href="/del/{{item['id']}}">削除</a>
  </div>
  
  %end


</div>


<div>
  <a href="/logout">ログアウト</a>
</div>
