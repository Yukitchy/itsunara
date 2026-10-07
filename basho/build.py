# src.html + SHOPS -> index.html（文節の切れ目を焼き込む。CSSは word-break:keep-all）
# 実行: /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 build.py
import re, json, html, budoux
parser = budoux.load_default_japanese_parser()

SHOPS = [
 dict(k="oudori", name="炭火焼鳥 逢鳥", kana="おうどり", genre="焼き鳥と水炊き",
      pitch="掘りごたつの完全個室で、ゆっくり座って話せます。",
      walk="メトロC3出口から1分", walk2="JR西口からは5分。立教通りに入ってすぐの地下1階",
      room="掘りごたつの完全個室", room2="4人から使えます。部屋の指定はできません",
      budget="6,000円から8,000円", smoke="全席禁煙", smoke_warn=False,
      hours="17:00から22:50", hours2="料理のラストオーダーは22:10（日曜と祝日は21:50）",
      seats="30席の小さな店", tb="13158727", site="https://oudori-ikebukuro.com/", ll="35.731514,139.706914"),
 dict(k="sora", name="池袋 寿司 個室 空", kana="そら", genre="寿司と海鮮",
      pitch="駅から1分。4人用の個室が2部屋だけの、静かな寿司屋です。",
      walk="東口から1分", walk2="フジビル7階",
      room="4人用の個室が2部屋", room2="ほかに2人用と3人用の個室",
      budget="6,000円から8,000円", smoke="全席禁煙", smoke_warn=False,
      hours="17:00から23:00", hours2="土日と祝日は16:00から。ラストオーダーは22:00。年中無休",
      seats="25席", tb="13250240", site="", ll="35.72879,139.712568"),
 dict(k="kushitei", name="串揚げ 串亭 ルミネ池袋", kana="くしてい", genre="串揚げ",
      pitch="駅とつながったルミネの8階。雨の日でも濡れずに着きます。",
      walk="池袋駅直結", walk2="ルミネ池袋の8階。エレベーターで上がれます",
      room="4人用の個室あり", room2="6人用と8人用もあります",
      budget="4,000円から5,000円", smoke="全席禁煙", smoke_warn=False,
      hours="11:00から22:00", hours2="料理のラストオーダーが21:00と早めです", hours_warn=True,
      seats="54席", tb="13139771", site="https://www.lumine.ne.jp/ikebukuro/floorguide/detail/?scd=000561", ll="35.728983,139.709605"),
 dict(k="irodori", name="いろどり 池袋", kana="いろどり", genre="野菜の肉巻き串と水炊き",
      pitch="色とりどりの野菜巻き串が名物。サンシャインの入口の正面です。",
      walk="東口から5分", walk2="サンシャインシティ入口の正面、サントロペビル7階",
      room="4人用の個室と半個室", room2="混んでいる日は2時間制のことがあります",
      budget="4,000円から5,000円", smoke="全席禁煙", smoke_warn=False,
      hours="17:00から22:30", hours2="土日と祝日は16:00から。料理のラストオーダーは21:50",
      seats="68席", tb="13240464", site="https://irodori-ikebukuro.com/", ll="35.730524,139.716438"),
 dict(k="shun", name="THE SUSHI TOKYO 旬", kana="しゅん", genre="寿司と日本料理のコース",
      pitch="完全個室でコースの寿司。ちょっといい日にしたい時に。",
      walk="池袋駅から3分", walk2="東池袋、池袋旗ビルの地下1階",
      room="完全個室", room2="4人用、6人用、8人用",
      budget="10,000円から15,000円", smoke="全席禁煙", smoke_warn=False,
      hours="17:00から23:00", hours2="最後に入れるのは21:00",
      seats="32席", tb="13294312", site="", ll="35.731995,139.713736"),
 dict(k="kotobuki", name="別邸 壽", kana="ことぶき", genre="しゃぶしゃぶとすき焼き",
      pitch="格子に囲まれた和の個室で、しゃぶしゃぶかすき焼き。",
      walk="西口（北口）から5分", walk2="平和通り、ドン・キホーテの近くの地下1階",
      room="4人用の個室", room2="個室料が1部屋2,000円かかります",
      budget="10,000円から15,000円", smoke="分煙", smoke2="個室の中では加熱式たばこが使えます", smoke_warn=True,
      hours="17:00から23:30", hours2="料理のラストオーダーは22:00",
      seats="60席", tb="13264867", site="https://bettei-kotobuki-ikebukuro.com/", ll="35.733779,139.71183"),
]

def phrase(inner):
    if not re.search(r'[ぁ-んァ-ヶ一-龠]', inner): return inner
    out = parser.translate_html_string(inner)
    out = re.sub(r'^<span style="[^"]*">(.*)</span>$', r'\1', out, flags=re.S)
    out = re.sub(r'​((?:<[^>]+>)*[」）、。？！])', r'\1', out)
    out = re.sub(r'([「（](?:<[^>]+>)*)​', r'\1', out)
    pat = re.compile(r'[「（]+[^\s​「（」）]|[^\s​「（][。、？！]*[」）][。、？！」）]*')
    return ''.join(p if p.startswith('<') else pat.sub(lambda m: f'<span class="nw">{m[0]}</span>', p) for p in re.split(r'(<[^>]+>)', out))

def shop(i, s):
    e = html.escape
    links = [f'<a href="https://tabelog.com/tokyo/A1305/A130501/{s["tb"]}/" target="_blank" rel="noopener">食べログで見る</a>']
    if s["site"]: links.append(f'<a href="{e(s["site"])}" target="_blank" rel="noopener">お店のサイト</a>')
    links.append(f'<a href="https://www.google.com/maps/search/?api=1&amp;query={s["ll"]}" target="_blank" rel="noopener">地図アプリで開く</a>')
    w = lambda cond: ' class="warn"' if cond else ''
    return f'''<article class="shop" id="s{i}">
<figure class="ph"><img src="img/{s["k"]}.jpg" alt="{e(s["name"])}の写真" loading="lazy" width="640" height="480"></figure>
<div class="body">
<span class="no num">{i}</span>
<h3>{e(s["name"])}</h3>
<p class="genre">{e(s["genre"])}</p>
<p class="pitch">{e(s["pitch"])}</p>
<dl class="facts">
<dt>駅から</dt><dd>{e(s["walk"])}<small>{e(s["walk2"])}</small></dd>
<dt>席</dt><dd>{e(s["room"])}<small>{e(s["room2"])}。{e(s["seats"])}</small></dd>
<dt>予算</dt><dd>1人 {e(s["budget"])}くらい<small>夜の食べログ目安</small></dd>
<dt>たばこ</dt><dd{w(s["smoke_warn"])}>{e(s["smoke"])}{f'<small>{e(s["smoke2"])}</small>' if s.get("smoke2") else ''}</dd>
<dt>夜の営業</dt><dd>{e(s["hours"])}<small{w(s.get("hours_warn"))}>{e(s["hours2"])}</small></dd>
</dl>
<div class="map"><iframe title="{e(s["name"])}の地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={s["ll"]}&amp;z=17&amp;output=embed"></iframe></div>
<div class="links">{"".join(links)}</div>
</div>
</article>'''

src = open("src.html").read()
src = src.replace("<!--SHOPS-->", "\n".join(shop(i+1, s) for i, s in enumerate(SHOPS)))
BLOCK = re.compile(r'(<(p|h1|h2|h3|dd|small|figcaption)(?:\s[^>]*)?>)(.*?)(</\2>)', re.S)
src = BLOCK.sub(lambda m: m[1] + phrase(m[3]) + m[4], src)
open("index.html", "w").write(src)
assert "—" not in src and "–" not in src
print("ok", len(src))
