# Flaskでブックマークアプリを作ろう（上巻・基礎編）

## 第0章 はじめに

このチュートリアルでは、Flaskを使ってブックマークアプリを作成します。  
筆者の開発環境は、Windows 11、Python 3.10、Flask 3.1.0です。  
コードエディタは、Visual Studio Codeです。  
以下、Visual Studio Code（VSCode）で作業を進めていくことを前提に説明します。

### このチュートリアルで作るもの

URLとタイトルを登録・編集・削除できるシンプルなブックマークアプリです。  
データはデータベースに保存し、登録したブックマークの一覧をWebブラウザで確認できます。

### 対象読者

- Pythonの基本的な文法（変数、関数、if文など）を理解している方  
- Webアプリ開発に興味があり、Flaskを初めて触る方  

HTML・CSSの基本的な知識があると、よりスムーズに進められるでしょう。
JavaScriptの知識については、必須ではありません。

### このチュートリアルについて

このチュートリアルは**上巻（基礎編）**と**下巻（応用編）**の2部構成です。  
本書（上巻）では、FlaskでCRUD機能を持つブックマークアプリを一から完成させることを目標とします。  
下巻では、アプリをより実践的な構成へと発展させていきます（Blueprintの導入、ファイル分割、タグ機能の追加など）。

### チュートリアルの構成

| 章 | 内容 |
| --- | --- |
| 第1章 | 最初のFlaskアプリを作成し、起動する |
| 第2章 | HTMLテンプレートを使ってWebページを表示する |
| 第3章 | 複数ページを作成し、ページ間の移動（ルーティング）を実装する |
| 第4章 | 各ページのモックアップとフォームパーツを作成する |
| 第5章 | データベースの導入 |
| 第6章 | データベースの操作(1) - データの追加と一覧表示 |
| 第7章 | データベースの操作(2) - データの編集と削除 |
| 第8章 | まとめ |

## 第1章 最初のFlaskアプリ

### 下準備 - Pythonと仮想環境のセットアップ

まずはPythonがインストールされていることを確認しましょう。ターミナルで以下のコマンドを実行してください。

```bash
python --version
```

Python 3.9以降がインストールされていればOKです。次に、プロジェクト用のディレクトリを作成し、その中で仮想環境をセットアップします。

```bash
mkdir flask-bookmarks
cd flask-bookmarks
python -m venv .venv
```

仮想環境を有効化します。

- Windowsの場合:

```bash
.venv\Scripts\activate
```

- macOS/Linuxの場合:

```bash
source .venv/bin/activate
```

### Flask, Flask-SQLAlchemyのインストール

仮想環境が有効になった状態で、**Flask** と **Flask-SQLAlchemy** をインストールしましょう。

```bash
pip install Flask Flask-SQLAlchemy
```

Flask-SQLAlchemyは、後の章でデータベース機能を実装する際に使用します。  
SQLAlchemyとはPythonでデータベースを扱うためのライブラリで、SQLを直接書かずにPythonのコードだけでデータの保存・取得ができます。  
Flask-SQLAlchemyは、それをFlask向けにより使いやすくしたものです。  
今すぐ使うわけではありませんが、ここでまとめてインストールしておきましょう。

### requirements.txtの作成

`requirements.txt` は、このプロジェクトで使用しているPythonパッケージの一覧をまとめたファイルです。  
以下のコマンドを実行すると、現在インストールされているパッケージが自動的にファイルへ書き出されます。

```bash
pip freeze > requirements.txt
```

作成された `requirements.txt` を開くと、次のような内容が記録されています（出力される内容は環境によって異なります）。

```text
blinker==1.9.0
click==8.1.8
colorama==0.4.6
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
greenlet==3.1.1
itsdangerous==2.2.0
Jinja2==3.1.5
MarkupSafe==3.0.2
SQLAlchemy==2.0.37
typing_extensions==4.12.2
Werkzeug==3.1.3
```

> [!NOTE]
> `pip freeze` はインストール済みのパッケージをすべて出力するコマンドです。  
> `>` は出力先をファイルに切り替える記号で、`requirements.txt` という名前のファイルに書き込まれます。

`requirements.txt` を作成しておくと、別の環境（別のPC、チームメンバーのPCなど）でも次の1コマンドだけで同じ環境を再現できます。

```bash
pip install -r requirements.txt
```

このように `requirements.txt` を使ったパッケージ管理は、Pythonプロジェクトの標準的な手法です。

### 最初のFlaskアプリを作成

プロジェクトディレクトリの中に `app.py` というファイルを作成し、以下のコードを追加してください。

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
```

このコードの各行の役割は以下の通りです。

- **`from flask import Flask`**: Webアプリケーションの土台となる機能を提供する「Flask」というライブラリから、メインの部品である `Flask` クラスをインポート（読み込み）します。
- **`app = Flask(__name__)`**: `Flask` クラスからアプリケーションの本体（インスタンス）を作成し、変数 `app` に代入します。`__name__` は現在のファイルがどこから実行されているかを示す特殊な変数で、Flaskが各種ファイル（テンプレートなど）の場所を正しく見つけるために必要です。
- **`@app.route('/')`**: 「**デコレータ**」と呼ばれる、関数にWeb上のURLを結びつける機能です。この記述により、ユーザーがブラウザでトップページ（ルートURL: `/`）にアクセスしたときに、すぐ下の関数が自動的に実行されるようになります。URLごとに別の関数を用意することで、ページごとに処理を分けることができます。
- **`def hello():`**: 実際に処理を行う関数です。この関数が `return` した文字列が、そのままブラウザの画面上に表示されます。この例では「Hello, Flask!」というテキストを返しています。
- **`app.run(debug=True)`**: `app.run` で開発用のウェブサーバーを起動し、アプリが立ち上がります。`debug=True` を指定することで、コードを書き換えて保存したときに自動でサーバーが再起動するため、ブラウザを更新（再読み込み）するだけで変更をすぐに確認できるようになります。

> [!WARNING]
> `debug=True` は開発環境でのみ使用してください。本番環境では `debug=False` に設定し、WSGIサーバー（例: Gunicorn）を使用してアプリを起動してください。デバッグモードを本番で有効にすると、エラーメッセージに詳細な情報が表示され、セキュリティリスク（情報漏洩など）が発生する可能性があります。

### アプリの起動

ターミナルで以下のコマンドを実行してアプリを起動します。

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセスすると、「Hello, Flask!」と表示されるはずです。これで最初のFlaskアプリが完成しました！次の章では、簡単なHTMLを表示するようにしましょう。

### アプリの終了方法

ターミナルで `Ctrl + C`（Macの場合 `Control + C`）を押すと、アプリを終了できます。  
`debug=True` の設定により、コードを変更して保存すると自動的に再起動しますが、
エラーが発生した際にサーバーが意図しない状態になることがあります。  
問題が起きたと感じたら、いったん `Ctrl + C` で終了して再起動することをおすすめします。

## 第2章 HTMLを表示する

### HTMLファイルの作成

プロジェクトディレクトリの中に `templates` という名前のフォルダを作成します。そして、その中に `index.html` というファイルを作成し、以下のコードを追加してください。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Flaskアプリ</title>
</head>
<body>
    <h1>Hello, Flask!</h1>
</body>
</html>
```

### Flaskアプリの修正

`app.py` を以下のように修正します。

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

- **`render_template`**: `templates` フォルダにある指定したHTMLファイルを読み込んで、ブラウザに表示するための関数です。

### アプリの再起動

ターミナルで `python app.py` を実行し、ブラウザで `http://localhost:5000` にアクセスすると、HTMLファイルが表示されるはずです。これでFlaskアプリでHTMLを表示できるようになりました！

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

## 第4章 ページのモックアップとフォームの作成

ここでは、各ページにデータを表示・入力するための「器」を作成します。  
データベースはまだ登場しませんが、後でデータを流し込めるよう、HTMLの構造だけ先に整えておきます。  
このチュートリアルではPythonとFlaskの動作が主体なので、HTMLのパーツ分けはできるだけ簡潔に、CSSはなるべく最小限にとどめます。

### ホームページ（index.html）の更新

ホームページには、登録されているブックマークの一覧をリスト形式で表示します。  
現在は「ここにブックマークの一覧を後で表示します。」というプレースホルダーだけが入っています。  
ここでは、後でデータベースから取得した内容を表示するためのリストのテンプレートをHTMLで作成します。

`templates/index.html` を以下のように書き換えます。

```html
{% extends "base.html" %}

{% block title %}ホーム - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマーク一覧</h2>

<ul class="bookmark-list">
  <li>
    <a class="bookmark-item-title" href="https://example.com" target="_blank">サンプルサイト</a>
    <div>
      <a class="btn btn-green" href="/edit">編集</a>
      <button type="button" class="btn btn-red">削除</button>
    </div>
  </li>
</ul>
{% endblock %}
```

今は実際のデータはなく、リストの構造を確認するためにサンプルのデータを1件だけ直接書いています（**ハードコーディング**）。  
リンク先（`href`）も仮のものを指定していますが、これらは後の章で Flask の便利な関数（`url_for`）やデータベースと連携したテンプレート構文に置き換えていきます。

#### ポイント：リストの構造

| タグ | 役割 |
| --- | --- |
| `<ul>` | 順序のないリスト全体を囲む（Unordered List） |
| `<li>` | リストの各項目を囲む（List Item） |
| `<a>` | リンクを作成する。`target="_blank"` で別のブラウザタブで開く |
| `<div>` | 複数の要素（リンクやボタン）をグループとしてまとめる |

> [!NOTE]
> 編集ボタンは `<a class="btn btn-green">` 、削除ボタンは `<button class="btn btn-red">` としています。
> 編集は「別のページ（/edit）へ移動するだけ」なので `<a>` タグ（リンク）を使い、削除は「データを消す」という動作を行う `<button>` タグを使います。
> タグは異なりますが、どちらも同じ `.btn` クラスを使ってボタン共通のスタイルを持たせることで、見た目を統一しています。
> そして、これらを `<div>` で囲み、一つの「ボタングループ」としてまとめています。
>
> [!TIP]
> **なぜクラスを使用するのか**
> ここで単に `<a>` タグに対してスタイルを適用（`.bookmark-list a`）してしまうと、その子要素にある「編集」ボタン（これも `<a>` タグ）にも意図せずタイトル用のスタイルが適用されてしまいます。
> 特定の要素だけにスタイルを適用したい場合は、このように一意のクラス名（`.bookmark-item-title` など）を付与して指定するのが基本です。

### 追加ページ（add.html）の更新

追加ページには、タイトルとURLを入力して登録するフォームを作ります。  
`templates/add.html` を以下のように書き換えます。

```html
{% extends "base.html" %}

{% block title %}追加 - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマークを追加</h2>

<form action="/add" method="post">
  <div>
    <label>タイトル</label>
    <input type="text" name="title" placeholder="サイト名" required>
  </div>

  <div>
    <label>URL</label>
    <input type="url" name="url" placeholder="https://example.com" required>
  </div>

  <div class="btn-group">
    <button type="submit" class="btn btn-blue">登録</button>
    <a class="btn btn-gray" href="/">キャンセル</a>
  </div>
</form>
{% endblock %}
```

#### ポイント：フォームの主な属性

| 属性・タグ | 役割 |
| --- | --- |
| `<form action="/add" method="post">` | フォームの送信先URLと送信方式（POST）を指定する |
| `<label>` | 入力項目のラベル（説明文） |
| `<input type="text">` | 1行のテキスト入力欄 |
| `<input type="url">` | URL専用の入力欄（書式チェックあり） |
| `name="..."` | サーバー側でデータを受け取るときに使う名前 |
| `required` | 入力必須項目にする（ブラウザ側のバリデーション） |
| `<button type="submit">` | フォームを送信するボタン |

`method="post"` は、入力したデータをサーバーに「送信」する方式です。  
後の章で Flask 側に POST リクエストを受け取る処理を追加することで、実際に登録できるようになります。

### 編集ページ（edit.html）の更新

編集ページは追加ページとほぼ同じ構造です。  
違いは、すでに登録されているデータが入力欄に入った状態で表示される点です（後の章で実装します）。  
`templates/edit.html` を以下のように書き換えます。

```html
{% extends "base.html" %}

{% block title %}編集 - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマークを編集</h2>

<form action="/edit" method="post">
  <div>
    <label>タイトル</label>
    <input type="text" name="title" value="サンプルサイト" required>
  </div>

  <div>
    <label>URL</label>
    <input type="url" name="url" value="https://example.com" required>
  </div>

  <div class="btn-group">
    <button type="submit" class="btn btn-blue">保存</button>
    <a class="btn btn-gray" href="/">キャンセル</a>
  </div>
</form>
{% endblock %}
```

追加ページとの違いは、`<input>` タグに `value="..."` 属性があることです。  
現時点ではサンプルの値を直接書いていますが、後でデータベースから取得した値を `{{ bookmark_item.title }}` のようなFlaskのテンプレート構文で埋め込みます。

### CSSの追加

現在の `static/style.css` は背景色とフォントの指定だけです。  
テーブルやフォームが見やすくなるよう、最小限のスタイルを追加します。  
`static/style.css` を以下のように書き換えます。

```css
/* 基本設定 */
* {
  /* input等が100%指定ではみ出さないための設定 */
  box-sizing: border-box;
}

body {
  background-color: #f0f0f0;
  font-family: sans-serif;
  padding: 20px;
  /* 画面が広いPCで見やすくするための設定 */
  max-width: 800px;
  margin: 0 auto;
}

/* ナビゲーション */
nav {
  margin-bottom: 20px;
}

nav a {
  margin-right: 10px;
  color: #007bff;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

/* ブックマークリスト */
.bookmark-list {
  list-style-type: none;
  padding: 0;
  margin-top: 10px;
}

.bookmark-list li {
  margin-bottom: 15px;
}

.bookmark-item-title {
  font-size: 1.1em;
  color: #007bff;
  text-decoration: none;
}

.bookmark-item-title:hover {
  text-decoration: underline;
}

/* フォーム */
form div {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* ボタン共通スタイル（<button>・<a>どちらにも使用） */
.btn {
  display: inline-block;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  color: #fff;
  text-decoration: none;
}

/* ボタン群の共通スタイル */
.btn-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

button.btn {
  line-height: normal;
}

.btn-green { background: #28a745; }
.btn-green:hover { background: #218838; }

.btn-red { background: #dc3545; }
.btn-red:hover { background: #c82333; }

.btn-blue { background: #007bff; }
.btn-blue:hover { background: #0056b3; }

.btn-gray { background: #6c757d; }
.btn-gray:hover { background: #5a6268; }
```

### 動作確認

`python app.py` を実行して動作確認しましょう。  
以下の点を確認してみてください。

1. `http://localhost:5000/` にアクセスすると、ブックマーク一覧のリストとナビゲーションリンクが表示されることを確認します。
2. 「追加」リンクをクリックすると、タイトルとURLの入力フォームが表示されることを確認します。
3. 「編集」リンクをクリックすると、固定値（サンプルデータ）が入力済みのフォームが表示されることを確認します。
4. 「登録する」「保存する」ボタンをクリックするとエラーになることを確認します（現時点ではサーバー側のデータ処理がないため、エラーで正常です）。

4番のエラーは想定内です。次の章以降でデータベースとFlaskの処理を追加することで、実際にデータを保存・更新できるようになります。  

これで各ページの「器」が整いました。次の章ではデータベースを導入して、実際にブックマークを保存できるようにしていきます。

## 第5章 データベースの導入

### データベースの選択

このチュートリアルでは、Flaskと親和性の高い **Flask-SQLAlchemy** を使用します。  
Flask-SQLAlchemyは第1章ですでにインストール済みなので、いよいよここで出番がやってきました。

第1章でも解説しましたが、Flask-SQLAlchemyは、SQLAlchemyというPythonのデータベースライブラリをFlask向けに使いやすくしたものです。

SQLを直接書かずに、Pythonのクラス（**モデル**）でテーブル構造を定義できるため、コードが読みやすく管理しやすくなります。  
また、データベースファイルには **SQLite** を使います。外部のサーバーが不要で、ファイル1つで動作するため、開発用途に最適です。

### app.pyの設定とモデルの定義

`app.py` を以下のように修正します。  
データベースの設定・モデルの定義・初期化の処理をまとめて追加します。

```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

#### app.py の解説

追加・変更した箇所を説明します。

- **`from flask_sqlalchemy import SQLAlchemy`**: Flask-SQLAlchemy をインポートします。
- **`app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'`**: データベースの場所を指定します。`sqlite:///` に続けてファイル名を書くと、プロジェクト内の `instance/` フォルダに `bookmarks.db` が自動的に作成されます。
- **`db = SQLAlchemy(app)`**: SQLAlchemy を Flask アプリと連携させます。この `db` オブジェクトを通じて、モデルの定義やデータベース操作を行います。

#### モデルの定義について

`Bookmark` クラスがデータベースのテーブル（`bookmark` テーブル）に対応します。  
`db.Model` を継承することで、このクラスがテーブルと紐づきます。

| カラム名 | 型 | 説明 |
| --- | --- | --- |
| `id` | `db.Integer` | 主キー（自動連番） |
| `title` | `db.String(200)` | ブックマークのタイトル（最大200文字） |
| `url` | `db.String(500)` | ブックマークのURL（最大500文字） |

### データベースの初期化

`app.py` を実行すると、`if __name__ == '__main__':` ブロック内の `db.create_all()` によって、テーブルが自動的に作成されます。

```bash
python app.py
```

実行後、プロジェクト内に `instance/bookmarks.db` ファイルが作成されます。  
`db.create_all()` はテーブルがすでに存在する場合は何もしないため、2回目以降の起動でデータが消えることはありません。

### データベースの確認

`python app.py` を実行すると、VSCodeの画面左側の**エクスプローラー**に `instance/bookmarks.db` ファイルが表示されます。  
このファイルが作成されていれば、データベースの初期化は成功です。

## 第6章 データベースの操作(1) - データの追加と一覧表示

### データベースの操作（CRUD）について

ここからはデータの追加・更新・削除を実装していきます。  
まずその前に、データベース操作の流れを軽く見ておきましょう。  
データベースの操作には **CRUD** という基本的な操作があります。  
CRUDとは、以下の4つの操作の頭文字をとったものです。

- **C**reate: 作成
- **R**ead: 読み込み
- **U**pdate: 更新
- **D**elete: 削除

この4つの操作をマスターすれば、データベースの操作はバッチリです！
この章では、**C**reateと**R**ead、すなわち「追加」と「一覧表示」を実装します。

### Create - データの追加

まずは、フォームから送られてきたデータをデータベースに追加する処理を実装します。

#### データの追加（app.pyの修正）

`app.py` を以下のように修正します。

```python
from flask import Flask, render_template, request, redirect, url_for # request, redirect, url_for を追加
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

# データの追加関数
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title'].strip()
        url = request.form['url'].strip()
        if not title or not url:
            return render_template('add.html')
        bookmark_item = Bookmark(title=title, url=url)
        db.session.add(bookmark_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

##### データの追加処理における変更点

大きく分けて2つの変更点があります。

- **`from flask import Flask, ...`**: `request`, `redirect`, `url_for` を追加でインポートしました。
- **`@app.route('/add', ...)`**: 新たに `add` 関数（データの追加処理）を定義しました。

##### request, redirect, url_for について

- **`request`**: クライアント（ブラウザ）から送信されたデータ（フォームの入力内容など）を受け取るために使用します。
- **`redirect`**: 処理が終わった後に、別のURLへ自動的に移動（リダイレクト）させるために使用します。
- **`url_for`**: 指定した関数名から、対応するURLを自動的に生成するために使用します。 `url_for` は、すでに第3章でHTMLファイルでは **jinja2** テンプレートの中で出てきていますが、それをPythonファイルでも利用できるようにするために `import` します。

##### データ追加 (add関数) の解説

新たに追加した `add` 関数の処理の流れを解説します。

```python
# データの追加関数
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title'].strip()
        url = request.form['url'].strip()
        if not title or not url:
            return render_template('add.html')
        bookmark_item = Bookmark(title=title, url=url)
        db.session.add(bookmark_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')
```

- **`@app.route('/add', methods=['GET', 'POST'])`**: `/add` というURLにアクセスした際の処理を定義します。`methods=['GET', 'POST']` を指定することで、GETメソッドとPOSTメソッドの両方を受け付けるようにしています。
- **`if request.method == 'POST':`**: アクセス時のHTTPメソッドが `POST` であるか（つまり、フォームからデータが送信されたか）を判定します。
- **`title = request.form['title'].strip()`**: 送信されたフォームデータの中から `name="title"` の値を取得します。`.strip()` を付けることで、前後の余計な空白を削除します。
- **`url = request.form['url'].strip()`**: 同様に `name="url"` の値を取得し、余計な空白を削除します。
- **`if not title or not url:`**: タイトルまたはURLが空（または空白のみ）でないかチェックします。もし空であれば、保存処理をせずに再度 `add.html` を表示（フォームを再表示）します。
- **`bookmark_item = Bookmark(title=title, url=url)`**: 受け取ったデータを使って、データベースに保存するための `Bookmark` クラスのインスタンス（新しいデータ）を作成します。
- **`db.session.add(bookmark_item)`**: 作成したデータをデータベースの保存準備状態（セッション）に追加します。
- **`db.session.commit()`**: データベースに変更を確定（保存）させます。
- **`return redirect(url_for('index'))`**: 保存が完了したら、`index` 関数に対応するURL（トップページ `/` ）へ移動します。
- **`return render_template('add.html')`**: GETメソッドの場合、ここではデータ追加用のフォームを表示するために `add.html` を表示します。

##### GETメソッドとPOSTメソッドについて

- **GETメソッド**: サーバーからデータを「取得」するために使用します。ブラウザのURLバーにアドレスを入力してページを表示するときや、リンクをクリックしたときは通常GETメソッドが使われます。
- **POSTメソッド**: サーバーへデータを「送信」するために使用します。今回のようにフォームに内容を入力して「登録」ボタンを押したときなどは、POSTメソッドが使われます。

#### ナビゲーションリンクの更新（base.htmlの修正）

`base.html` のナビゲーション（リンクメニュー）も更新しましょう。
直接 URL（`/add`）を書く代わりに、Flask の `url_for` 関数を使う形に修正します。

`templates/base.html` の `<nav>` 部分を見つけて、以下のように修正します（ホームのリンクも忘れずに `url_for` を使います）。

```html
  <nav>
    <a href="{{ url_for('index') }}">ホーム</a>
    <a href="{{ url_for('add') }}">追加</a>
  </nav>
```

これにより、リンクをクリックした際に確実に対応する関数（この場合はデータの追加ページを表示する `add` 関数）にアクセスして `add.html` が表示されるようになります。

##### データ追加の動作確認

ここまで記述できたら、一旦アプリを起動（または再読み込み）してブラウザで確認してみましょう。
ナビゲーションの「追加」リンクをクリックして追加ページ（`/add`）を開き、フォームにタイトルとURLを入力して「登録する」ボタンを押してみてください。
エラーにならずにホーム画面（`/`）へ戻ってくれば成功です！
（追加したデータが一覧に表示されるかどうかは、次の「Read」節で確認します。）

### Read - データの表示

データをデータベースから取得して `index.html` で表示できるように修正します。

#### データの表示（app.pyの修正）

まず、`app.py` の `index()` 関数を修正し、データベースから取得したデータを `index.html` に渡すようにします。

```python
@app.route('/')
def index():
    bookmark_list = Bookmark.query.all()
    return render_template('index.html', bookmark_list=bookmark_list)
```

##### `index()` 関数の解説

すべてのデータを取得する `bookmark_list` 変数を追加し、`render_template` の第2引数で `index.html` に渡します。
`Bookmark.query.all()` は、`Bookmark` モデルに対応するデータベーステーブルから、登録されているすべてのデータを取得します。  
取得したデータはリスト形式で返されます。

#### データの表示（index.htmlの修正）

次に `index.html` の `<ul>` タグを修正します。  
（第4章で作成したリンクメニューやリスト構造も残しつつ、リストの中身をテンプレート構文に置き換えます）

```html
{% extends "base.html" %}

{% block title %}ホーム - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマーク一覧</h2>

<ul class="bookmark-list">
  {% for bookmark_item in bookmark_list %}
    <li>
      <a href="{{ bookmark_item.url }}" target="_blank" class="bookmark-item-title">{{ bookmark_item.title }}</a>
      <div class="btn-group">
        <a class="btn btn-green" href="/edit">編集</a>
        <button type="button" class="btn btn-red">削除</button>
      </div>
    </li>
  {% else %}
    <li>まだブックマークが登録されていません。</li>
  {% endfor %}
</ul>
{% endblock %}
```

##### `index.html` の変更点

今回のポイントは、第4章で**ハードコーディング**していたリスト部分を **Jinja2** のループ構文に置き換えた点です。

- **`{% for bookmark_item in bookmark_list %}`**: Flask の `index()` 関数から渡された `bookmark_list` リストの件数分ループ処理します。
- **`<a href="{{ bookmark_item.url }}" target="_blank">{{ bookmark_item.title }}</a>`**: ブックマークのタイトルをクリックすると元の URL へ移動します。`target="_blank"` で新しいタブで開きます。
- **`{% else %}`**: `bookmark_list` リストが空の場合（まだブックマークがない場合）に表示される分岐です。
- **`{% endfor %}`**: ループを終了します。

##### データの表示の動作確認

ここまで記述できたら、アプリを起動（または再読み込み）してブラウザで確認してみましょう。
ホーム画面（`/`）にアクセスし、先ほどの「データの追加の動作確認」で入力したブックマークが一覧に表示されていれば成功です！

これまではブラウザの表示を確認しても、再起動すると消えてしまう「一時的な表示」でしたが、データベースを使うことで、アプリを再起動しても登録したデータが残り、一覧に表示され続けるようになります。

次章では、この一覧に「編集」と「削除」の機能を追加して、CRUD操作を完成させていきます。

## 第7章 データベースの操作(2) - データの編集と削除

### データを編集・削除するためのボタンを作成する

一覧表示している `templates/index.html` のリスト構造のなかに、編集と削除のボタンを配置します。  
第4章で `index.html` を作成した際にすでに編集と削除ボタンの骨組みは作成済みですが、ここでは機能とデザインを追加します。  

#### 編集・削除ボタンの追加（index.htmlの修正）

以下のコードを参考に、`index.html` の `<ul class="bookmark-list">...</ul>` の部分を修正してください。

```html
{% extends "base.html" %}

{% block title %}ホーム - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマーク一覧</h2>

<ul class="bookmark-list">
  {% for bookmark_item in bookmark_list %}
    <li>
      <a href="{{ bookmark_item.url }}" target="_blank" class="bookmark-item-title">{{ bookmark_item.title }}</a>
      <div class="btn-group">
        <a class="btn btn-green" href="{{ url_for('edit', id=bookmark_item.id) }}">編集</a>
        <button type="button" class="btn btn-red">削除</button>
      </div>
    </li>
  {% else %}
    <li>まだブックマークが登録されていません。</li>
  {% endfor %}
</ul>
{% endblock %}
```

##### 追加したボタンのコード解説

第4章で「器」として作成したボタンを、Jinja2テンプレートを使って動的に機能させています。

- **`href="{{ url_for('edit', id=bookmark_item.id) }}"`**: 固定で記述していた `href="/edit"` の部分を、データのIDを含めたURLを生成するように変更しています。 `url_for` 関数を使い、`edit` 関数（編集ページ）へのURLを生成しています。引数に `id=bookmark_item.id` を渡すことで、特定のデータを指定するURL（例：`/edit/1`）が作成されます。
- **タグの使い分けとクラス**: 第4章で解説した通り、編集は移動を伴うため `<a>` タグ、削除は処理を実行するため `<button>` タグを使用しています。見た目は `.btn` クラスで統一し、役割に応じた色（`btn-green`, `btn-red`）を適用しています。

#### CSSで見た目を整える

このままでは、追加したボタンの見た目が少し味気ないことに加え、配置も少し崩れてしまいます。そこで `static/style.css` の末尾に以下のCSSコードを追加・修正し、リストの整列とボタンのデザインを整えましょう。

（※ 既存の `.bookmark-list li` に関する指定がある場合は、以下の内容で上書きするか、適宜内容を差し替えてください。）

```css
/* リスト項目の横並び配置 */
.bookmark-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}
```

これでリストがきれいに整列し、ボタンも分かりやすくクリックしやすいデザインになりました。

### Update - データの編集

#### 編集処理（app.pyの修正）

既存の `edit` 関数を修正して、データの編集処理を行えるようにします。

`app.py` の `@app.route('/edit')` から始まる `edit` 関数を次のように書き換えてください。

```python
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    bookmark_item = Bookmark.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        url = request.form['url'].strip()
        if not title or not url:
            return render_template('edit.html', bookmark_item=bookmark_item)
        bookmark_item.title = title
        bookmark_item.url = url
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', bookmark_item=bookmark_item)
```

##### 編集処理コードの解説

- **`@app.route('/edit/<int:id>', ...)`**: URLの中に `<int:id>` を含めることで、アクセスしたURLの一部を変数 `id` として関数に渡すことができます。（例: `/edit/1` なら `id=1`）
- **`Bookmark.query.get_or_404(id)`**: データベースから指定したIDのデータを取得します。もし見つからなければ、自動的に「404 Not Found（ページが見つかりません）」エラーを返してくれる便利な関数です。
- **データの上書きと保存**: `POST`（保存するボタンが押された）の場合、フォームから送られてきた `title` と `url` で `bookmark_item` のデータを上書きします。その後、追加の時と同じく `db.session.commit()` を呼ぶことで、データベースへの変更（更新）が確定されます。

#### 編集画面テンプレートの修正（edit.htmlの修正）

次に、取得したデータを編集フォームの初期値として表示するため、第4章で仮で作成していた `templates/edit.html` を修正します。

各 `<input>` タグの `value` 属性に、データベースから取得した `bookmark_item` の値を設定します。また、`<form action="/edit" ...>` の部分も修正し、該当データのIDが含まれたURLに送信するようにします。

`templates/edit.html` 全体のコードを以下のように書き換えてください。

```html
{% extends "base.html" %}

{% block title %}編集 - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマークを編集</h2>

<form action="{{ url_for('edit', id=bookmark_item.id) }}" method="post">
  <div>
    <label>タイトル</label>
    <input type="text" name="title" value="{{ bookmark_item.title }}" required>
  </div>

  <div>
    <label>URL</label>
    <input type="url" name="url" value="{{ bookmark_item.url }}" required>
  </div>

  <div class="btn-group">
    <button type="submit" class="btn btn-blue">保存</button>
    <a class="btn btn-gray" href="{{ url_for('index') }}">キャンセル</a>
  </div>
</form>
{% endblock %}
```

##### 編集機能の動作確認

これで編集機能の実装が完了しました。ターミナルで `python app.py` を再実行（または起動中ならブラウザを再読み込み）し、動作を確認してみましょう。

1. 一覧画面の「編集」ボタンをクリックする
2. タイトルやURLを変更して「保存する」ボタンをクリックする
3. ホーム画面に戻り、内容が正しく更新されていれば成功です！

残るは「削除」機能だけです。引き続き追加していきましょう。

### Delete - データの削除

#### 削除処理（app.pyの修正）

データの削除処理を行うための `delete` 関数を追加します。

`app.py` の `edit` 関数の下（または末尾）に、次のコードを追加してください。

```python
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    bookmark_item = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark_item)
    db.session.commit()
    return redirect(url_for('index'))
```

##### 削除処理コードの解説

- **`@app.route('/delete/<int:id>', methods=['POST'])`**: 追加（add）・編集（edit）との違いは、`GET` メソッドはなく、`POST` メソッドのみを扱うことです。URLの部分は `edit` 関数と同様に `<int:id>` を含めており、削除したいデータのIDを表します。
- **`Bookmark.query.get_or_404(id)`**: この部分も `edit` 関数と同じです。データベースから指定したIDのデータを取得し、もし見つからなければ、自動的に「404 Not Found（ページが見つかりません）」エラーを返します。
- **`db.session.delete(bookmark_item)`**: データベースから指定したIDのデータを削除します。
- **`db.session.commit()`**: データベースへの変更（削除）が確定されます。

#### 削除ボタンをフォームに変更する（index.htmlの修正）

`delete` 関数は `POST` メソッドのみを受け付けます。しかし現状の `index.html` の削除ボタンは `<button type="button">` のままで、`/delete/<int:id>` へ POST リクエストを送れません。  
`index.html` の削除ボタン部分を、フォームで囲んだ形に修正しましょう。

`templates/index.html` の削除ボタン部分を以下のように書き換えます。

```html
<form action="{{ url_for('delete', id=bookmark_item.id) }}" method="post">
  <button type="submit" class="btn btn-red">削除</button>
</form>
```

`index.html` 全体のコードは次のとおりです。

```html
{% extends "base.html" %}

{% block title %}ホーム - Bookmark App{% endblock %}

{% block content %}
<h2>ブックマーク一覧</h2>

<ul class="bookmark-list">
  {% for bookmark_item in bookmark_list %}
    <li>
      <a href="{{ bookmark_item.url }}" target="_blank" class="bookmark-item-title">{{ bookmark_item.title }}</a>
      <div class="btn-group">
        <a class="btn btn-green" href="{{ url_for('edit', id=bookmark_item.id) }}">編集</a>
        <form action="{{ url_for('delete', id=bookmark_item.id) }}" method="post">
          <button type="submit" class="btn btn-red">削除</button>
        </form>
      </div>
    </li>
  {% else %}
    <li>まだブックマークが登録されていません。</li>
  {% endfor %}
</ul>
{% endblock %}
```

##### 削除機能の動作確認

これで削除機能の実装が完了しました。ターミナルで `python app.py` を再実行（または起動中ならブラウザを再読み込み）し、動作を確認してみましょう。

1. 一覧画面の「削除」ボタンをクリックする
2. ホーム画面に戻り、該当のブックマークが削除されていれば成功です！

## 第8章 まとめ

お疲れ様でした！これで上巻のチュートリアルはすべて完了です。

### 完成したプロジェクトの構成

最終的なプロジェクトのフォルダ・ファイル構成は次のとおりです。

```text
flask-bookmarks/
├── app.py
├── requirements.txt
├── instance/
│   └── bookmarks.db
├── static/
│   ├── style.css
│   └── main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── add.html
    └── edit.html
```

### 完成した app.py

チュートリアルを通じて少しずつ育ててきた `app.py` の最終的な全体コードは次のとおりです。

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

@app.route('/')
def index():
    bookmark_list = Bookmark.query.all()
    return render_template('index.html', bookmark_list=bookmark_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title'].strip()
        url = request.form['url'].strip()
        if not title or not url:
            return render_template('add.html')
        bookmark_item = Bookmark(title=title, url=url)
        db.session.add(bookmark_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    bookmark_item = Bookmark.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title'].strip()
        url = request.form['url'].strip()
        if not title or not url:
            return render_template('edit.html', bookmark_item=bookmark_item)
        bookmark_item.title = title
        bookmark_item.url = url
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', bookmark_item=bookmark_item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    bookmark_item = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark_item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

### 上巻で学んだこと

| 概念 | 内容 |
| --- | --- |
| 仮想環境・パッケージ管理 | `venv` で環境を分離し、`requirements.txt` で依存関係を管理する |
| ルーティング | `@app.route` でURLと処理する関数を対応させる |
| テンプレート（Jinja2） | `render_template` と `{% block %}` 構文でHTMLを動的に生成する |
| 静的ファイル | `static` フォルダにCSS・JavaScriptを置き、`url_for` で参照する |
| データベース（Flask-SQLAlchemy） | `db.Model` を継承したクラスでテーブルを定義する |
| CRUD操作 | Create / Read / Update / Delete の4つの基本操作を実装する |
| GETとPOSTメソッド | フォームの表示（GET）とデータ送信（POST）の使い分け |

### 下巻へのプレビュー

上巻では、1つの `app.py` にすべての処理をまとめて書いてきました。  
小規模なアプリではこれで十分ですが、機能が増えていくと `app.py` が肥大化し、読みにくく管理しにくくなっていきます。

下巻（応用編）では、より実践的な開発スタイルへと発展させていきます。

> **下巻（応用編）で扱う予定のテーマ**
>
> - **Blueprint の導入**: アプリを機能単位でファイルに分割し、コードを整理する
> - **app.py のリファクタリング**: データベース設定やモデルを別ファイルに切り出す
> - **フラッシュメッセージ**: 「登録しました」などの操作結果をユーザーに通知する
> - **タグ機能の追加**: ブックマークにタグをつけて分類する（多対多のリレーション）

引き続き下巻もよろしくお願いします！
