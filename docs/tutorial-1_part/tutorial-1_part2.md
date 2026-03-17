# Flaskでブックマークアプリを作ろう（上巻・基礎編）第1章

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
