%rebase("base.tpl",title="できたできた！")
%include('header_dekita.tpl')

<div class="container">
    <div class="dekita_main hanko_relative" id="dekita_hanko">

        <form action="/add" method="POST">
            <input type="text" size="30" maxlength="50" id="dekita_input" autocomplete="off" name="dekita" placeholder="あなたの「できた」を教えて。"><br>
            <input class="btn" type="submit" id="dekita_submit" name="save" value="できた！">
        </form>
        <img src="static/img/hanko_dekita.png">

        <h2>{{user_name_tpl}}さんの<br>これまでの「できたできた」：{{sum_tpl}}</h2>
        <h3>今日のできたできた：{{sum_today_tpl}}</h3>
        <p class="ymd">{{dekita_list_tpl[0]["ymd"]}} {{dekita_list_tpl[0]["youbi"]}}</p>

        %check = dekita_list_tpl[0]["ymd"]
        %i = 3

        %for item in dekita_list_tpl:
        %if item["ymd"] != check:
        <p class="ymd">{{item["ymd"]}} {{item["youbi"]}}</p>
        %check = item["ymd"]
        %i = 3
        %end
        <div class="dekita_group">
            <a href="/detail/{{item['id']}}">
                <span class="dekita_circle">
                    %if i%3 == 0:
                    %i = i + 1
                    で
                    %elif i%3 == 1:
                    %i = i + 1
                    き
                    %elif i%3 == 2:
                    %i = i + 1
                    た
                    %end
                </span>
                <span class="dekita_memo">{{item["dekita"]}}</span>
                <span class="dekita_time">{{item["msm"]}}</span>
            </a>
        </div>
        %end

    </div>
    <div class="back">
        <a href="#dekita_input">
            <img src="static/img/kuma2.png" alt="#">
        </a>
    </div>
</div>