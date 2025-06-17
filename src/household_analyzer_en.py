import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from datetime import datetime

class HouseholdAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load household budget data from CSV file"""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        self.df = pd.read_csv(self.csv_path)
        self.df['Date'] = pd.to_datetime(self.df['日付'])
        self.df['Month'] = self.df['Date'].dt.to_period('M')
        self.df['Net'] = self.df['収入'] - self.df['支出']
        
        # Translate categories to English
        category_map = {
            '収入': 'Income',
            '食費': 'Food',
            '光熱費': 'Utilities',
            '交通費': 'Transportation',
            '娯楽': 'Entertainment',
            '日用品': 'Daily Goods',
            '医療費': 'Medical'
        }
        self.df['Category'] = self.df['カテゴリ'].map(category_map)
        
        print(f"Data loaded: {len(self.df)} records")
        print(f"Period: {self.df['Date'].min()} to {self.df['Date'].max()}")
    
    def monthly_summary(self):
        """Create monthly income/expense summary"""
        monthly = self.df.groupby('Month').agg({
            '収入': 'sum',
            '支出': 'sum',
            'Net': 'sum'
        }).round(0)
        
        monthly.columns = ['Income', 'Expense', 'Net']
        return monthly
    
    def category_summary(self):
        """Create category-wise expense summary"""
        expenses = self.df[self.df['支出'] > 0]
        category_summary = expenses.groupby('Category')['支出'].sum().sort_values(ascending=False)
        return category_summary
    
    def plot_monthly_trend(self, figsize=(12, 8)):
        """Create monthly income/expense trend chart"""
        monthly = self.monthly_summary()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, height_ratios=[2, 1])
        
        # Income, Expense, Net trend
        x = range(len(monthly))
        ax1.plot(x, monthly['Income'], marker='o', linewidth=2, label='Income', color='green')
        ax1.plot(x, monthly['Expense'], marker='s', linewidth=2, label='Expense', color='red')
        ax1.plot(x, monthly['Net'], marker='^', linewidth=2, label='Net', color='blue')
        
        ax1.set_title('Monthly Income/Expense Trend', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Amount (Yen)', fontsize=12)
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(x)
        ax1.set_xticklabels([str(month) for month in monthly.index], rotation=45)
        
        # Income/Expense ratio
        income_ratio = monthly['Income'] / (monthly['Income'] + monthly['Expense']) * 100
        expense_ratio = monthly['Expense'] / (monthly['Income'] + monthly['Expense']) * 100
        
        ax2.bar(x, income_ratio, label='Income Ratio', color='green', alpha=0.7)
        ax2.bar(x, -expense_ratio, label='Expense Ratio', color='red', alpha=0.7)
        
        ax2.set_title('Income/Expense Ratio', fontsize=14)
        ax2.set_ylabel('Ratio (%)', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(x)
        ax2.set_xticklabels([str(month) for month in monthly.index], rotation=45)
        ax2.axhline(y=0, color='black', linewidth=0.5)
        
        plt.tight_layout()
        return fig
    
    def plot_category_pie(self, figsize=(10, 8)):
        """Create category-wise expense pie chart"""
        category_data = self.category_summary()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(category_data)))
        wedges, texts, autotexts = ax.pie(
            category_data.values, 
            labels=category_data.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        
        ax.set_title('Expense Distribution by Category', fontsize=16, fontweight='bold')
        
        # Make percentage text more visible
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        return fig
    
    def plot_category_bar(self, figsize=(12, 6)):
        """Create category-wise expense bar chart"""
        category_data = self.category_summary()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        bars = ax.bar(category_data.index, category_data.values, 
                     color=plt.cm.viridis(np.linspace(0, 1, len(category_data))))
        
        ax.set_title('Expense by Category', fontsize=16, fontweight='bold')
        ax.set_ylabel('Expense (Yen)', fontsize=12)
        ax.set_xlabel('Category', fontsize=12)
        
        # Add values on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'¥{int(height):,}',
                   ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return fig
    
    def plot_daily_spending(self, figsize=(14, 6)):
        """Create daily spending trend chart"""
        daily_expenses = self.df[self.df['支出'] > 0].groupby('Date')['支出'].sum()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(daily_expenses.index, daily_expenses.values, 
               marker='o', linewidth=1, markersize=4, alpha=0.7)
        
        ax.set_title('Daily Spending Trend', fontsize=16, fontweight='bold')
        ax.set_ylabel('Expense (Yen)', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        
        # Add moving average
        rolling_mean = daily_expenses.rolling(window=7).mean()
        ax.plot(rolling_mean.index, rolling_mean.values, 
               color='red', linewidth=2, label='7-day Moving Average')
        
        ax.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def generate_report(self):
        """Generate analysis report"""
        print("=" * 50)
        print("Household Budget Analysis Report")
        print("=" * 50)
        
        # Basic statistics
        total_income = self.df['収入'].sum()
        total_expense = self.df['支出'].sum()
        net_amount = total_income - total_expense
        
        print(f"\n【Overall Summary】")
        print(f"Total Income: ¥{total_income:,}")
        print(f"Total Expense: ¥{total_expense:,}")
        print(f"Net Amount: ¥{net_amount:,}")
        print(f"Savings Rate: {(net_amount/total_income)*100:.1f}%")
        
        # Monthly summary
        print(f"\n【Monthly Summary】")
        monthly = self.monthly_summary()
        print(monthly.to_string())
        
        # Category summary
        print(f"\n【Expense by Category】")
        category = self.category_summary()
        for cat, amount in category.items():
            percentage = (amount / total_expense) * 100
            print(f"{cat:15s}: ¥{amount:8,.0f} ({percentage:5.1f}%)")
        
        print("=" * 50)

def main():
    # Data file path
    data_path = Path(__file__).parent.parent / "data" / "household_budget.csv"
    
    # Initialize analyzer
    analyzer = HouseholdAnalyzer(data_path)
    
    # Generate report
    analyzer.generate_report()
    
    # Generate and save charts
    print("\nGenerating charts...")
    
    # Monthly trend
    fig1 = analyzer.plot_monthly_trend()
    fig1.savefig('monthly_trend_en.png', dpi=300, bbox_inches='tight')
    print("Monthly trend chart saved: monthly_trend_en.png")
    
    # Category pie chart
    fig2 = analyzer.plot_category_pie()
    fig2.savefig('category_pie_en.png', dpi=300, bbox_inches='tight')
    print("Category pie chart saved: category_pie_en.png")
    
    # Category bar chart
    fig3 = analyzer.plot_category_bar()
    fig3.savefig('category_bar_en.png', dpi=300, bbox_inches='tight')
    print("Category bar chart saved: category_bar_en.png")
    
    # Daily spending trend
    fig4 = analyzer.plot_daily_spending()
    fig4.savefig('daily_spending_en.png', dpi=300, bbox_inches='tight')
    print("Daily spending trend saved: daily_spending_en.png")
    
    plt.show()

if __name__ == "__main__":
    main()