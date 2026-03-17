# Flaskでブックマークアプリを作ろう（上巻・基礎編）第3章

## 第3章 Webページの作成とルーティング

ここでは、先ほど作成したWebページに、ヘッダーとフッターを追加して、Webページのひな型を作成します。また、ルーティングを使って、Webページにアクセスしたときに表示される内容を切り替えられるようにします。

### HTML、CSS、JavaScriptの準備

ここでは、アプリ全体の共通レイアウトとなる `base.html` と、ブックマークを追加・編集するための `add.html`, `edit.html` を準備します。  
まずは必要なディレクトリと、基本的なHTMLファイル、CSSファイル、JavaScriptファイルを作成します。  
細かい機能は後で順を追って追加していきます。

#### 1. フォルダの準備

プロジェクトのルートディレクトリに、以下のフォルダを準備します。

第2章で作成した `templates` フォルダに加え、新たに `static` フォルダを作成してください。  
それぞれのフォルダの役割は以下の通りです。

- **`templates`**: HTMLファイルを置くフォルダ。
- **`static`**: CSSやJavaScript、画像などを置くフォルダ

#### 2. HTMLテンプレートの作成

`templates` フォルダの中に、以下の3つのファイルを作成します。

##### 共通レイアウト: `templates/base.html`

すべてのページの基本となるファイルです。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Bookmark App{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <nav>
    <a href="/">ホーム</a>
  </nav>

  <main>
    {% block content %}{% endblock %}
  </main>

  <script src="{{ url_for('static', filename='main.js') }}"></script>
</body>
</html>
```

ここで使われている特別な記法について簡単に説明します。
これらは **Jinja2** という、Flaskで標準採用されているテンプレートエンジンの機能です。

- **`{% block 名前 %}`**: 子テンプレートで中身を書き換えるための「場所」を指定します。
- **`{{ url_for('static', filename='...') }}`**: `url_for` は、指定したファイルやページにアクセスするためのURLを自動生成する関数です。この例では `static` フォルダ内のファイル（CSSやJSなど）のパスを作成しています。直接 `/static/style.css` と書くよりも、後からファイルの場所やアプリのURL構成が変わった際に柔軟に対応できるというメリットがあります。この `url_for` は非常に便利な機能なので、以降の章でも度々登場します。

##### 追加画面: `templates/add.html`

```html
{% extends "base.html" %}

{% block title %}追加 - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマークを追加</h2>
<p>ここにフォームを後で作成します。</p>
{% endblock %}
```

- **`{% extends "base.html" %}`**: このテンプレートが `base.html` を「継承」することを宣言します。これにより、`base.html` に書かれたHTMLの骨組み（`<head>` や `<nav>` など）をそのまま引き継ぎつつ、`{% block ... %}` の部分だけをこのページ専用の内容に書き換えることができます。

##### 編集画面: `templates/edit.html`

```html
{% extends "base.html" %}

{% block title %}編集 - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマークを編集</h2>
<p>ここに編集フォームを後で作成します。</p>
{% endblock %}
```

##### 最初のページ: `templates/index.html`

トップページである `index.html` も `base.html` を継承するようにします。  
以下のように書き換えましょう。  
`<head>` や `<body>` タグは `base.html` にすべてお任せなので、これだけで済みます。

```html
{% extends "base.html" %}

{% block title %}ホーム - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマーク一覧</h2>
<p>ここにブックマークの一覧を後で表示します。</p>
{% endblock %}
```

#### 3. 静的ファイルの作成

`static` フォルダの中に、以下の2つのファイルを作成します。

##### スタイルシート: `static/style.css`

動作確認のために、背景色だけ少し変えてみましょう。  
今はとりあえずこれだけですが、後でCSSを追加してデザインを整えていきます。

```css
body {
  background-color: #f0f0f0;
  font-family: sans-serif;
}
```

##### JavaScriptコード: `static/main.js`

ブラウザのコンソールにメッセージが出るようにします。

```javascript
console.log("Bookmark App loaded!");
```

`console.log()` は、ブラウザの **開発者ツール（コンソール）** にメッセージを表示するための命令です。  
動作確認や値の確認など、プログラミングにおいて非常によく使う手法です。  
このチュートリアルではJavaScriptについて詳しく触れませんが、Flaskアプリ開発でも必要になる場面があるため、基本的な操作を知っておくと便利です。

コンソールの開き方は以下の通りです。

| ブラウザ | 開き方 |
| --- | --- |
| Chrome / Edge | `F12` キー、または画面を右クリック →「検証」から「Console」タブを選択 |
| Firefox | `F12` キー、または画面を右クリック →「要素を調査」から「コンソール」タブを選択 |

コンソールを開くと、以下のようにメッセージが出力されているのを確認できます。

```text
Bookmark App loaded!
```

このように `console.log()` を使うと、JavaScriptが正しく読み込まれているかを手軽に確認できます。

これで、最低限の見た目と構成が整いました。次のステップでは、これらのファイルを実際に表示するための「**ルーティング**」を `app.py` に追加していきます。

### ルーティングの追加

各ページに対応するルーティングを追加します。

`app.py` を以下のように修正します。

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)
```

#### コードの解説

第1章の「最初のFlaskアプリを作成」でデコレータ `@app.route('/')` について説明しましたが、ここで少しおさらいします。  

- **`@app.route('/')`**: `'/'`（ルート）、すなわちトップページにアクセスしたときに、すぐ下の関数 `index()` を実行するように指示するものでした（第1章でも登場した内容です）。  
- 同じように、今回追加した `@app.route('/add')` と `@app.route('/edit')` は、それぞれ `'/add'`、`'/edit'` にアクセスしたときに対応する関数（`add()` と `edit()`）を実行するよう指示します。

アプリを起動して各URLにアクセスすると、それぞれの関数が実行され、`render_template()` によって対応したHTMLファイルがブラウザに表示される仕組みです。

これを踏まえて、実際にルーティングの動作を確認してみましょう。

### ルーティングの確認

ターミナルで `python app.py` を実行し、以下の手順でページが表示されるか確認します。

1. **ホーム画面の確認**
   ブラウザで `http://localhost:5000/` にアクセスします。`index()` 関数が実行され、`index.html` が表示されるはずです。
2. **追加画面の確認**
   URL欄の末尾に `/add` を追加して `http://localhost:5000/add` にアクセスします。`add()` 関数が実行され、`add.html` が表示されます。
3. **編集画面の確認**
   同様に、URL欄の末尾に `/edit` を追加して `http://localhost:5000/edit` にアクセスします。`edit()` 関数が実行され、`edit.html` が表示されるはずです。

### リンクメニューの追加

このままでは、URL欄に直接URLを入力しないとページを移動できません。  
そこで、すべてのページで共通して表示されるよう、`base.html` にリンクメニューを追加して、ページ間を移動できるようにします。  
`base.html` の `<nav>` タグ内に、以下を追加します。

```html
  <nav>
    <a href="/">ホーム</a>
    <a href="/add">追加</a>
  </nav>
```

※ `/edit` へのリンクは、後で編集機能のボタンとして配置するため、今は追加しません。

#### リンクメニューの動作確認

ターミナルで `python app.py` を実行して、動作確認してみましょう。
トップページの上部にリンクメニューが表示され、それぞれのリンクをクリックすると、それぞれのページに移動できるはずです。
