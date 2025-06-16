# high-school-python-vibe-coding-template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

- [`ハイスクールPython`](https://high-school-python.jp) の、Python の Vibe Coding 用のテンプレートです。
- [GitHub Repository](https://github.com/high-school-python/high-school-python-vibe-coding-template)

## ディレクトリ構成

このようなディレクトリ構成になっています

```sh
high-school-python-vibe-coding-template/    # このリポジトリのルートディレクトリ
├── .cursor/                # Cursor AI 設定ファイル
│   └── rules/              # Cursor 用のコーディング規約
├── .vscode/                # VSCode の設定ファイル
├── src/                    # ソースコード (uv 環境で実行可能)
│   ├── __init__.py         # Python パッケージファイル
│   └── hello.py            # サンプルスクリプト
├── CLAUDE.md               # Claude Code 用の設定ファイル
├── LICENSE                 # MIT ライセンス
├── README.md               # このファイル (説明書)
├── pyproject.toml          # uv の設定ファイル
└── uv.lock                 # 依存関係の固定ファイル
```

## 開発環境の構築

### 1. uv のインストール

このリポジトリでは、パッケージ管理に [uv](https://docs.astral.sh/uv/) を使用しています。まずはこちらの内容に従って、PC に uv をインストールしてください。

```sh
# Windows の場合
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac の場合
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. パッケージのインストール

以下のコマンドを実行してください。すると、`pyproject.toml` に記載されているパッケージがインストールされます。仮想環境は、`.venv/` に作成されます。

```sh
uv sync
```

パッケージを追加する場合は、以下のように `uv add` コマンドを使用してください。

```sh
# requests を追加
uv add requests

# 開発環境のみに追加
uv add --dev types-requests

# アップデート
uv add --upgrade requests
```

### 3. スクリプトの実行

以下のように、`uv run python -m` コマンドを使用して、スクリプトを実行できます。

```sh
uv run python -m src.hello
```

## コード品質管理

このプロジェクトでは、以下のツールを使用してコード品質を管理しています。

### リンティング・フォーマット

```sh
# コードのフォーマット
uv run ruff format

# リントチェック
uv run ruff check

# 自動修正
uv run ruff check --fix
```

### 型チェック

```sh
# 型チェック実行
uv run mypy src/
```

### テスト実行

```sh
# テスト実行
uv run pytest
```

### 一括品質チェック

```sh
# すべてのチェックを一括実行
uv run ruff check && uv run ruff format && uv run mypy src/
```

## Vibe Coding

このプロジェクトは AI コーディングアシスタントによる開発支援に対応しています：

### Cursor 対応

参考 URL: <https://docs.cursor.com/context/rules>

- `.cursor/rules/` ディレクトリに、プロジェクト固有のコーディング規約を設定
- Python 学習者向けの最適化されたコード生成ルールを適用
- 科学計算ライブラリの使用パターンを自動的に適用

### Claude Code 対応

参考 URL: <https://docs.anthropic.com/ja/docs/claude-code/overview>

- `CLAUDE.md` ファイルにプロジェクト情報とコマンドを記載
- 開発ワークフローと環境設定の詳細を提供
