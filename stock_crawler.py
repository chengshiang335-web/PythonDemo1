import requests
import pandas as pd
from datetime import datetime, timedelta
import json

def get_twse_stock_data(stock_id, start_date=None, end_date=None):
    """
    爬取台灣證交所股票資訊
    
    Args:
        stock_id: 股票代碼 (例如: 2330 為台積電)
        start_date: 開始日期 (YYYY-MM-DD 格式)
        end_date: 結束日期 (YYYY-MM-DD 格式)
    """
    
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"正在爬取股票代碼: {stock_id}")
    print(f"日期範圍: {start_date} 至 {end_date}")
    print("-" * 60)
    
    all_data = []
    
    # 轉換日期格式為 YYYYMMDD
    start_date_str = start_date.replace('-', '')
    end_date_str = end_date.replace('-', '')
    
    # 台灣證交所查詢歷史資訊 API
    url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=&stockNo={stock_id}&_=1591519963209"
    
    try:
        # 嘗試使用 yfinance (推薦方式)
        import yfinance as yf
        
        ticker = yf.Ticker(f"{stock_id}.TW")
        df = ticker.history(start=start_date, end=end_date)
        
        if df.empty:
            print(f"❌ 無法獲取股票 {stock_id} 的數據")
            return None
        
        # 重新命名欄位並格式化
        df_result = df.copy()
        df_result.columns = ['開盤價', '最高價', '最低價', '收盤價', '成交量', '股利', '股票分割比例']
        df_result['日期'] = df_result.index.strftime('%Y-%m-%d')
        df_result = df_result[['日期', '開盤價', '最高價', '最低價', '收盤價', '成交量']]
        
        print(f"\n✅ 成功爬取 {len(df_result)} 筆資料")
        print("\n" + "="*60)
        print(df_result.to_string())
        print("="*60)
        
        # 統計資訊
        print("\n📊 統計資訊:")
        print(f"平均收盤價: {df_result['收盤價'].mean():.2f}")
        print(f"最高價: {df_result['最高價'].max():.2f}")
        print(f"最低價: {df_result['最低價'].min():.2f}")
        print(f"總成交量: {df_result['成交量'].sum():,.0f}")
        
        return df_result
        
    except ImportError:
        print("❌ 需要安裝 yfinance 模組")
        print("執行命令: pip install yfinance")
        return None
    except Exception as e:
        print(f"❌ 爬取失敗: {str(e)}")
        return None


def main():
    # 爬取台積電 (2330) 過去 60 天的交易資訊
    result = get_twse_stock_data(
        stock_id='2330',
        start_date='2026-01-10',
        end_date='2026-02-25'
    )
    
    if result is not None:
        # 顯示最新的交易日資訊
        if not result.empty:
            latest = result.iloc[-1]
            print(f"\n🔔 最新交易日: {latest['日期']}")
            print(f"   收盤價: {latest['收盤價']:.2f}")
            print(f"   成交量: {latest['成交量']:,.0f}")
        
        # 可選: 存存為 CSV 檔案
        result.to_csv('stock_2330.csv', index=False, encoding='utf-8-sig')
        print("\n💾 資料已存存至 stock_2330.csv")


if __name__ == "__main__":
    main()
