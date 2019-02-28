%rebase("base.tpl",title="月木でわかる HTML5 &amp; CSS3")

	<article>
		<section id="sec1">
			<h1>月木でわかる <br> HTML5 &amp; CSS3</h1>
		</section>

		<section id="sec2">
			<h1>3つのブロックエリア<br>flexとの上手な付き合い方</h1>
			<div class="box flex_area">
				<div class="flex_area_padding">
					<h2>flexを使って左から詰めていく</h2>
					<p>ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります
					</p>
				</div>
				<div class="flex_area_padding">
					<h2>flexを使って左から詰めていく</h2>
					<p>ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります
					</p>
				</div>
				<div class="flex_area_padding">
					<h2>flexを使って左から詰めていく</h2>
					<p>ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります
					</p>
				</div>
			</div>
		</section>

		<section id="sec3">
			<div class="box">
				<h1>まずはお聞かせ下さい<br>御社の"中央寄せ"について</h1>
				<p>PC版では段落を整えるために改行したい。しかしSP版では不用意な改行を入れたくない。そんな時はbrをdisplay:noneすると良いでしょう。</p>
				<p>テキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキスト。</p>
				<p>
					テキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキスト。<br> テキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキスト
				</p>
				<p>
					テキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキスト、<br> テキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテキストテ、
					<br> テキストテキストテキストテキストテキストテキストテキストテキストテキス
					<br> テキストテキストテキストテキストテキストテキストテキストテキストテキストテキ。
				</p>
			</div>
		</section>

		<section id="sec4">
			<div class="box port">
				<h1>制作実績</h1>
				<p>ここでもdisplay:flexの練習をしましょうdisplay:flexは様々な並び替えをすることができます。<br> グリッドレイアウトと言われるCSSも最近流行っています。ここではflexを使用します。
				</p>

				<!-- 追加した箇所↓ -->
				<button id="size-up">画像拡大</button>
				<button id="img-change">画像変更</button>
				<!-- 追加した箇所、以上 -->

				<!-- FadeThis用のクラスを追加 -->
				<div class="portfolio slide-bottom" data-plugin-options='{"speed":1000 , "reverse": false}'>
					<a href="#"><img src="static/img/thumb_01.png" alt="あいうえお">
						<p class="port_title">あいうえお建設様</p>
					</a>
					<p class="port_margin">ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。 ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。
					</p>
				</div>

				<div class="portfolio flex_reverse slide-bottom" data-plugin-options='{"speed":1000 , "reverse": false}'>
					<p class="port_margin">ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。 ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。
					</p>
					<a href="#"><img src="static/img/thumb_02.png" alt="かきくけこ">
						<p class="port_title">かきくけこ電気様</p>
					</a>
				</div>

				<div class="portfolio slide-bottom" data-plugin-options='{"speed":1000 , "reverse": false}'>
					<a href="#"><img src="static/img/thumb_03.png" alt="さしすせそ">
						<p class="port_title">さしすせそ興行様</p>
					</a>
					<p class="port_margin">ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。 ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。ここに制作実績のテキストが入ります。
					</p>
				</div>

			</div>
		</section>
	</article>
