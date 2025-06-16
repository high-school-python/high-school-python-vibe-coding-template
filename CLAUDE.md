# CLAUDE.md

このファイルは、このリポジトリでコードを操作する際の Claude Code (claude.ai/code) へのガイダンスを提供します。

## プロジェクト概要

これは「ハイスクール Python」のバイブコーディングセッション用の Python テンプレートです。科学計算ライブラリを使った Python プログラミング学習環境として設計されています。

## 開発環境

このプロジェクトは、パッケージ管理と Python 環境管理に **uv** を使用しています。

### 基本コマンド

```bash
# 環境のセットアップと依存関係のインストール
uv sync

# Pythonスクリプトの実行
uv run python -m src.hello
uv run python -m src.[モジュール名]

# Streamlitアプリケーション実行
uv run streamlit run src/[アプリファイル名].py

# 新しい依存関係の追加
uv add [パッケージ名]

# 開発用依存関係の追加
uv add --dev [パッケージ名]

# コード品質チェック
uv run ruff check
uv run ruff format
uv run mypy src/

# テストの実行
uv run pytest
```

## アーキテクチャ

- **src/**: すべての Python ソースコードを格納
  - 完全なカリキュラムではレッスン別に整理（lesson_1/, lesson_2/, など）
  - 各レッスンには番号付きの Python ファイル（1-1.py, 1-2.py, など）を含む
  - 各レッスンには Jupyter notebook（.ipynb）が付随
- **依存関係**: 科学計算・Web開発スタック（numpy, pandas, matplotlib, scikit-learn, scipy, streamlit）
- **開発ツール**: ruff（リンティング/フォーマット）、mypy（型チェック）、pytest（テスト）

## Python 環境

- **Python バージョン**: 3.13+
- **パッケージマネージャー**: uv（pip/conda ではない）
- **仮想環境**: uv によって.venv/で自動管理
