# Flaskでブックマークアプリを作ろう（上巻・基礎編）第6章

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
- **POSTメソッド**: サーバーへデータを「送信」するために使用します。今回のようにフォームに内容を入力して「登録」ボタンを押したときなどは, POSTメソッドが使われます。

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
