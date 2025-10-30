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