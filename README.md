# 家計簿分析ツール 💰

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red.svg)](https://streamlit.io/)

Pythonを使って家計簿データを「良い感じに」グラフ化するツールです。

## 🎯 機能

- 📈 **月別収支トレンド**: 収入・支出・純額の推移を可視化
- 🥧 **カテゴリ別分析**: 支出内訳を円グラフと棒グラフで表示
- 📅 **日別支出パターン**: 移動平均付きの日々の支出トレンド
- 🔥 **ヒートマップ**: 曜日別支出パターンの可視化
- 📊 **統計レポート**: 貯蓄率、カテゴリ別サマリーなど
- 🎛️ **インタラクティブダッシュボード**: フィルター機能付きのWebアプリ

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
# 依存関係のインストール
uv sync
```

### 2. 基本分析を実行

```bash
# コマンドライン版（統計レポート + 静的グラフ生成）
uv run python -m src.household_analyzer_en
```

### 3. インタラクティブダッシュボードを起動

```bash
# Webダッシュボード
uv run streamlit run src/household_dashboard.py
```

ブラウザで `http://localhost:8501` にアクセスしてダッシュボードを操作できます。

## 📁 ファイル構成

```
src/
├── household_analyzer_en.py    # メイン分析プログラム
├── household_dashboard.py      # Streamlitダッシュボード
└── hello.py                   # サンプルファイル

data/
└── household_budget.csv       # サンプル家計簿データ
```

## 📊 データ形式

CSVファイルは以下の形式で作成してください：

```csv
日付,カテゴリ,項目,収入,支出
2024-01-01,収入,給料,300000,0
2024-01-02,食費,スーパー,0,5000
2024-01-03,交通費,電車,0,1200
```

### カラム説明

- **日付**: YYYY-MM-DD形式
- **カテゴリ**: 収入、食費、光熱費、交通費、娯楽、日用品、医療費など
- **項目**: 具体的な内容（給料、スーパー、電車など）
- **収入**: 収入金額（支出の場合は0）
- **支出**: 支出金額（収入の場合は0）

## 🎨 生成されるグラフ

### コマンドライン版
実行すると以下のPNGファイルが生成されます：

- `monthly_trend_en.png` - 月別収支トレンド
- `category_pie_en.png` - カテゴリ別円グラフ
- `category_bar_en.png` - カテゴリ別棒グラフ
- `daily_spending_en.png` - 日別支出トレンド

### ダッシュボード版
インタラクティブな機能：

- 📅 **期間フィルター**: 特定期間のデータを表示
- 🏷️ **カテゴリフィルター**: 特定カテゴリのみ表示
- 📋 **データテーブル**: 生データの確認
- 📊 **詳細統計**: 月別・カテゴリ別サマリー

## 💡 使用例

### 自分の家計簿データを使う場合

1. `data/household_budget.csv` を自分のデータに置き換え
2. 上記のデータ形式に合わせてCSVを作成
3. プログラムを実行

### カテゴリをカスタマイズしたい場合

`src/household_analyzer_en.py` の `category_map` を編集：

```python
category_map = {
    '収入': 'Income',
    '食費': 'Food', 
    '光熱費': 'Utilities',
    '新カテゴリ': 'New Category'  # 追加
}
```

## 🛠️ 技術スタック

- **Python 3.13+**: プログラミング言語
- **uv**: パッケージマネージャー
- **pandas**: データ処理
- **matplotlib**: 静的グラフ生成
- **plotly**: インタラクティブグラフ
- **streamlit**: Webダッシュボード

## 📖 開発環境

### コード品質管理

```bash
# コードのフォーマット
uv run ruff format

# リントチェック
uv run ruff check

# 型チェック
uv run mypy src/
```

### Vibe Coding対応

このプロジェクトは AI コーディングアシスタントによる開発支援に対応：

- **Cursor**: `.cursor/rules/` でコーディング規約を設定
- **Claude Code**: `CLAUDE.md` でプロジェクト情報を管理

## 🤝 コントリビューション

プルリクエストや Issue の報告を歓迎します！

---

**Made with ❤️ for [ハイスクールPython](https://high-school-python.jp)**