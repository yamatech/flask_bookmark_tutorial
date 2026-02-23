# 🔖 Bookmark App

Flaskで作ったシンプルなブックマーク共有アプリです。
同じLAN（ローカルネットワーク）内であれば、複数のブラウザ・デバイスから同じブックマークにアクセスできます。

## セットアップ & 起動

`.venv` が未作成でも起動スクリプトが自動でセットアップします。
初回は仮想環境の作成とパッケージのインストールが行われ、2回目以降はそのまま起動します。

### Mac / Linux / WSL / Git Bash

初回のみ、実行権限を付与してください。

```bash
chmod +x run.sh
```

その後は以下のコマンドで起動します。

```bash
./run.sh
```

### Windows（コマンドプロンプト）

```bat
run.bat
```

起動後、ブラウザで `http://localhost:5000` を開いてください。

---

> **手動でセットアップする場合**

```bash
> python3 -m venv .venv
> source .venv/bin/activate       # Windows: .venv\Scripts\activate
> pip install -r requirements.txt
> python app.py
```

## 複数デバイスで共有する方法

`app.py` は `host='0.0.0.0'` で起動するため、**同じWi-Fi/LAN内の他のデバイスからもアクセス可能**です。

1. サーバーを起動しているPCのIPアドレスを確認します
   - Mac/Linux: `ifconfig` または `ip a`
   - Windows: `ipconfig`
2. 他のデバイス（別のPC）のブラウザで `http://<IPアドレス>:5000` を開きます

例: `http://192.168.1.10:5000`

## 機能

- ✅ ブックマークの追加（タイトル・URL・タグ・メモ）
- ✅ タグでサイドバーフィルタリング
- ✅ タイトル・URL・メモで全文検索
- ✅ 編集・削除
- ✅ ファビコン自動取得
- ✅ SQLAlchemy + SQLiteでデータ永続化

## 技術スタック

| 種別 | 内容 |
| ------ | ------ |
| バックエンド | Python / Flask |
| ORM | Flask-SQLAlchemy |
| データベース | SQLite |
| フロントエンド | HTML / CSS / Vanilla JS |
| フォント | Syne, DM Sans (Google Fonts) |

## ファイル構成

```code
bookmark_app/
├── run.sh              # 起動スクリプト（Mac / Linux / WSL / Git Bash 用）
├── run.bat             # 起動スクリプト（Windows コマンドプロンプト用）
├── app.py              # アプリファクトリ (create_app) と起動
├── models.py           # db インスタンスと Bookmark モデル
├── routes.py           # Blueprint で全ルートを定義
├── requirements.txt    # 依存パッケージ
├── db/
│   └── bookmarks.db    # SQLiteデータベース（起動時に自動生成）
├── .venv/              # 仮想環境（起動スクリプトが自動生成）
├── static/
│   ├── style.css       # 全ページ共通スタイル
│   └── main.js         # 追加パネルの開閉
└── templates/
    ├── index.html      # ブックマーク一覧ページ
    └── edit.html       # 編集ページ
```

## ルート一覧

| メソッド | パス | 説明 |
| ---------- | ------ | ------ |
| GET | `/` | 一覧表示（タグ・キーワードフィルタ対応） |
| POST | `/add` | ブックマーク追加 |
| GET/POST | `/edit/<id>` | ブックマーク編集 |
| POST | `/delete/<id>` | ブックマーク削除 |
