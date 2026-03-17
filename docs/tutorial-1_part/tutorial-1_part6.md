# Flaskでブックマークアプリを作ろう（上巻・基礎編）第5章

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
