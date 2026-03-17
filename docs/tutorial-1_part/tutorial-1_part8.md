# Flaskでブックマークアプリを作ろう（上巻・基礎編）第7章

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
- **`Bookmark.query.get_or_404(id)`**: データベースから指定したIDのデータを取得します。もし見つからなければ, 自動的に「404 Not Found（ページが見つかりません）」エラーを返してくれる便利な関数です。
- **データの上書きと保存**: `POST`（保存するボタンが押された）の場合、フォームから送られてきた `title` と `url` で `bookmark_item` のデータを上書きします。その後, 追加の時と同じく `db.session.commit()` を呼ぶことで, データベースへの変更（更新）が確定されます。

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
