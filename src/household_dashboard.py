import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import numpy as np
from datetime import datetime
# import japanize_matplotlib

# ページ設定
st.set_page_config(
    page_title="家計簿ダッシュボード",
    page_icon="💰",
    layout="wide"
)

@st.cache_data
def load_data():
    """データを読み込む（キャッシュ付き）"""
    data_path = Path(__file__).parent.parent / "data" / "household_budget.csv"
    
    if not data_path.exists():
        st.error(f"データファイルが見つかりません: {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    df['日付'] = pd.to_datetime(df['日付'])
    df['月'] = df['日付'].dt.to_period('M').astype(str)
    df['純額'] = df['収入'] - df['支出']
    
    return df

def create_monthly_trend_chart(df):
    """月別トレンドチャートを作成"""
    monthly = df.groupby('月').agg({
        '収入': 'sum',
        '支出': 'sum',
        '純額': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly['月'], 
        y=monthly['収入'],
        mode='lines+markers',
        name='収入',
        line=dict(color='green', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly['月'], 
        y=monthly['支出'],
        mode='lines+markers',
        name='支出',
        line=dict(color='red', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly['月'], 
        y=monthly['純額'],
        mode='lines+markers',
        name='純額',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='月別収支トレンド',
        xaxis_title='月',
        yaxis_title='金額 (円)',
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_category_pie_chart(df):
    """カテゴリ別円グラフを作成"""
    expenses = df[df['支出'] > 0]
    category_data = expenses.groupby('カテゴリ')['支出'].sum().reset_index()
    
    fig = px.pie(
        category_data, 
        values='支出', 
        names='カテゴリ',
        title='カテゴリ別支出割合'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    return fig

def create_category_bar_chart(df):
    """カテゴリ別棒グラフを作成"""
    expenses = df[df['支出'] > 0]
    category_data = expenses.groupby('カテゴリ')['支出'].sum().sort_values(ascending=True)
    
    # カラーパレットを生成
    colors = px.colors.qualitative.Set3[:len(category_data)]
    
    fig = go.Figure(go.Bar(
        x=category_data.values,
        y=category_data.index,
        orientation='h',
        marker_color=colors
    ))
    
    fig.update_layout(
        title='カテゴリ別支出額',
        xaxis_title='支出額 (円)',
        yaxis_title='カテゴリ',
        height=500
    )
    
    return fig

def create_daily_spending_chart(df):
    """日別支出チャートを作成"""
    daily_expenses = df[df['支出'] > 0].groupby('日付')['支出'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_expenses['日付'],
        y=daily_expenses['支出'],
        mode='lines+markers',
        name='日別支出',
        line=dict(color='orange', width=2),
        marker=dict(size=4)
    ))
    
    # 移動平均を追加
    daily_expenses['移動平均'] = daily_expenses['支出'].rolling(window=7, center=True).mean()
    fig.add_trace(go.Scatter(
        x=daily_expenses['日付'],
        y=daily_expenses['移動平均'],
        mode='lines',
        name='7日移動平均',
        line=dict(color='red', width=3)
    ))
    
    fig.update_layout(
        title='日別支出トレンド',
        xaxis_title='日付',
        yaxis_title='支出額 (円)',
        height=500
    )
    
    return fig

def create_heatmap(df):
    """支出ヒートマップを作成"""
    expenses = df[df['支出'] > 0].copy()
    expenses['曜日'] = expenses['日付'].dt.day_name()
    expenses['週'] = expenses['日付'].dt.isocalendar().week
    
    pivot_data = expenses.groupby(['週', '曜日'])['支出'].sum().unstack(fill_value=0)
    
    # 曜日の順序を調整
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(columns=weekdays, fill_value=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=['月', '火', '水', '木', '金', '土', '日'],
        y=pivot_data.index,
        colorscale='Reds',
        showscale=True
    ))
    
    fig.update_layout(
        title='週別・曜日別支出ヒートマップ',
        xaxis_title='曜日',
        yaxis_title='週',
        height=400
    )
    
    return fig

def main():
    st.title("💰 家計簿ダッシュボード")
    st.markdown("---")
    
    # データ読み込み
    df = load_data()
    if df is None:
        return
    
    # サイドバー
    st.sidebar.header("フィルター")
    
    # 期間選択
    min_date = df['日付'].min().date()
    max_date = df['日付'].max().date()
    
    date_range = st.sidebar.date_input(
        "期間を選択",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # カテゴリ選択
    categories = ['全て'] + list(df['カテゴリ'].unique())
    selected_category = st.sidebar.selectbox("カテゴリ", categories)
    
    # データフィルタリング
    filtered_df = df.copy()
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['日付'].dt.date >= date_range[0]) & 
            (filtered_df['日付'].dt.date <= date_range[1])
        ]
    
    if selected_category != '全て':
        filtered_df = filtered_df[filtered_df['カテゴリ'] == selected_category]
    
    # メトリクス表示
    col1, col2, col3, col4 = st.columns(4)
    
    total_income = filtered_df['収入'].sum()
    total_expense = filtered_df['支出'].sum()
    net_amount = total_income - total_expense
    savings_rate = (net_amount / total_income * 100) if total_income > 0 else 0
    
    with col1:
        st.metric("総収入", f"¥{total_income:,.0f}")
    
    with col2:
        st.metric("総支出", f"¥{total_expense:,.0f}")
    
    with col3:
        st.metric("純額", f"¥{net_amount:,.0f}")
    
    with col4:
        st.metric("貯蓄率", f"{savings_rate:.1f}%")
    
    st.markdown("---")
    
    # グラフ表示
    tab1, tab2, tab3, tab4 = st.tabs(["📈 トレンド", "🥧 カテゴリ分析", "📅 日別分析", "🔥 ヒートマップ"])
    
    with tab1:
        st.subheader("月別収支トレンド")
        if len(filtered_df) > 0:
            fig = create_monthly_trend_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("選択された期間にデータがありません")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("カテゴリ別支出割合")
            if len(filtered_df[filtered_df['支出'] > 0]) > 0:
                fig = create_category_pie_chart(filtered_df)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("カテゴリ別支出額")
            if len(filtered_df[filtered_df['支出'] > 0]) > 0:
                fig = create_category_bar_chart(filtered_df)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("日別支出トレンド")
        if len(filtered_df[filtered_df['支出'] > 0]) > 0:
            fig = create_daily_spending_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("支出パターン分析")
        if len(filtered_df[filtered_df['支出'] > 0]) > 0:
            fig = create_heatmap(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
    
    # データテーブル
    st.markdown("---")
    st.subheader("📋 データテーブル")
    
    # 表示オプション
    show_income = st.checkbox("収入を表示", value=True)
    show_expense = st.checkbox("支出を表示", value=True)
    
    display_df = filtered_df.copy()
    if not show_income:
        display_df = display_df[display_df['収入'] == 0]
    if not show_expense:
        display_df = display_df[display_df['支出'] == 0]
    
    st.dataframe(
        display_df[['日付', 'カテゴリ', '項目', '収入', '支出', '純額']].sort_values('日付', ascending=False),
        use_container_width=True
    )
    
    # 統計サマリー
    if st.checkbox("詳細統計を表示"):
        st.subheader("📊 統計サマリー")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**月別サマリー**")
            monthly_summary = filtered_df.groupby('月').agg({
                '収入': 'sum',
                '支出': 'sum',
                '純額': 'sum'
            })
            st.dataframe(monthly_summary)
        
        with col2:
            st.write("**カテゴリ別サマリー**")
            if len(filtered_df[filtered_df['支出'] > 0]) > 0:
                category_summary = filtered_df[filtered_df['支出'] > 0].groupby('カテゴリ')['支出'].agg(['sum', 'mean', 'count'])
                category_summary.columns = ['合計', '平均', '回数']
                st.dataframe(category_summary.sort_values('合計', ascending=False))

if __name__ == "__main__":
    main()