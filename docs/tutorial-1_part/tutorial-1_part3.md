# Flaskでブックマークアプリを作ろう（上巻・基礎編）第2章

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
