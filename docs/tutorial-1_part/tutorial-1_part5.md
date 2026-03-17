# Flaskでブックマークアプリを作ろう（上巻・基礎編）第4章

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
