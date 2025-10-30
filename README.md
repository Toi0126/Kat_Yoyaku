# Kat_Yoyaku

Webサイトの予約情報を自動取得するスクリプトです。  
このリポジトリは、**どの環境でも即実行可能** な構成を目指しています。

---

## 🚀 動作確認環境
- Windows 10 / 11
- Python 3.12 以上
- PowerShell 5.1 以上

---

## 🧩 セットアップ手順

PowerShellを開き、以下のコマンドを**上から順に実行**してください。

```powershell
# 1️⃣ uv（パッケージ管理ツール）のインストール
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2️⃣ 仮想環境を作成（Pythonパスは環境に合わせて変更）
C:\hogehoge\Python312\python.exe -m venv .venv
# 例:
# C:\Users\PC_User\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv

# 3️⃣ 仮想環境を有効化
.\.venv\Scripts\activate

# 4️⃣ 依存関係を同期（pyproject.tomlから）
uv sync
```

# 5️⃣ 環境変数の設定
`.env` ファイルを作成し、以下の内容を記述してください。
```
BUCKET_NAME=line-bot-images-bucket
LINE_API_URL=https://api.line.me/v2/bot/message/push
ACCESS_TOKEN=あなたのアクセストークン
USER_ID=あなたのユーザーID
# AWS 資格情報（S3へ画像をアップロードする場合に必須）
AWS_ACCESS_KEY_ID=あなたのアクセスキーID
AWS_SECRET_ACCESS_KEY=あなたのシークレットアクセスキー
AWS_DEFAULT_REGION=ap-southeast-2
```

# 🧪 コード品質チェック・型チェック・テスト

```powershell
# コードスタイルチェック（ruff）
uv run ruff check

# 型チェック（mypy）
uv run mypy .\kat_yoyaku\

# テスト実行（pytest）
uv run pytest
```

# 🕷️ 実行方法
```powershell
# 仮想環境を有効化してから
.\.venv\Scripts\activate

# Webスクレイピングの実行
uv run python .\kat_yoyaku\kat_yoyaku.py
```

## 🧰 トラブルシュート

- 「認証情報が見つかりません。」が表示される場合
	- `.env` に `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` が設定されているか確認してください。
	- PowerShellで永続設定する場合（ユーザー環境変数）:
		```powershell
		setx AWS_ACCESS_KEY_ID "xxxxxxxx"
		setx AWS_SECRET_ACCESS_KEY "yyyyyyyy"
		setx AWS_DEFAULT_REGION "ap-southeast-2"
		```
		設定後はターミナルを再起動してください。
	- 付与すべき最小権限の例（S3）: `s3:PutObject`, `s3:PutObjectAcl`（public-readを使う場合）, `s3:ListBucket`（任意）
	- バケットのリージョンが `.env` の `AWS_DEFAULT_REGION` と一致しているか確認してください。

# 📁 フォルダ構成例

```bash
Kat_Yoyaku/
│
├─ kat_yoyaku/
│   ├─ __init__.py
│   ├─ kat_yoyaku.py          # メインスクリプト（Webスクレイピング）
│
├─ tests/
│   ├─ test_kat_yoyaku.py     # pytest用テストファイル
│
├─ pyproject.toml             # uv / ruff / mypy設定
├─ README.md                  # 本ドキュメント
```