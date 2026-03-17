# Flaskでブックマークアプリを作ろう（上巻・基礎編）第8章

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
