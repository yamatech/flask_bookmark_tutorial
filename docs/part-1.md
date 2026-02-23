# Flaskでブックマークアプリを作ろう

## 第1章 最初のFlaskアプリ

### 下準備 - Pythonと仮想環境のセットアップ

まずはPythonがインストールされていることを確認しましょう。ターミナルで以下のコマンドを実行してください。

```bash
python --version
```

Python 3.8以降がインストールされていればOKです。次に、プロジェクト用のディレクトリを作成し、その中で仮想環境をセットアップします。

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

### Flaskのインストール

仮想環境が有効になった状態で、Flaskをインストールします。

```bash
pip install Flask
```

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

### アプリの起動

ターミナルで以下のコマンドを実行してアプリを起動します。

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセスすると、「Hello, Flask!」と表示されるはずです。これで最初のFlaskアプリが完成しました！次の章では、データベースを使ってブックマークを保存する方法を学びましょう。
