%rebase("base.tpl")

<form action="/edit" method="POST">
<input type="text" value="{{tpl_item['id']}}" name="task_id">
<input type="text" value="{{tpl_item['task']}}" name="task">
<input type="submit" name="edit" value="編集する">
</form>