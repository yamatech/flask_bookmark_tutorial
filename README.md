# Flask Bookmark Tutorial

このプロジェクトは、Flaskフレームワークを使用したシンプルなブックマーク管理アプリケーションのチュートリアルです。ユーザーがブックマークを追加、編集、削除できる基本的な機能を備えています。

チュートリアルのドキュメントは[こちら](docs/tutorial-1.md)を参照してください。

## 概要

このチュートリアルでは、Pythonの軽量WebフレームワークであるFlaskを使用して、データベース（SQLite）と連携したWebアプリケーションの構築方法を学びます。

### 技術スタック

- **バックエンド**: Flask (Python)
- **データベース**: SQLite / SQLAlchemy
- **フロントエンド**: HTML, CSS (Jinja2 テンプレート)

### 機能

- ブックマークの追加
- ブックマークの編集
- ブックマークの削除
- ブックマークの一覧表示

## サンプルアプリケーションについて

サンプルアプリケーションのソースは[こちら](application/)にあります。ソースコードは全てチュートリアルドキュメントのコードに基づいて作成されています。アプリケーションは、ユーザーがブックマークを管理できるシンプルなインターフェースを提供します。
このリポジトリをクローンして、ローカル環境で実行することができます。

```bash
git clone

cd flask-bookmark-tutorial/application/

python -m venv venv

source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`

pip install -r requirements.txt

python app.py
```

ブラウザで `http://localhost:5000` にアクセスして、アプリケーションを使用できます。
