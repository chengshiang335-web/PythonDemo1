import requests
import pandas as pd
from datetime import datetime, timedelta
import json

def get_realtime_stock_price(stock_id):
    """
    獲取即時股票行情 (台灣證交所)
    """
    print(f"\n🔍 正在獲取 {stock_id} 的即時行情...")
    
    try:
        # 台灣證交所 API - 取得即時股票資訊
        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG_ALL?response=json&stockNo={stock_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                stock_data = data['data'][0]
                print(f"\n✅ 即時股價資訊:")
                print(f"   股票代碼: {stock_data[0]}")
                print(f"   現在時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   資料時間: {stock_data[1]}")
                return stock_data
        
        print(f"❌ 無法獲取即時行情")
        return None
        
    except Exception as e:
        print(f"❌ 獲取即時行情失敗: {str(e)}")
        return None


def get_twse_stock_data(stock_id, start_date=None, end_date=None):
    """
    爬取台灣證交所股票資訊
    """
    
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"正在爬取股票代碼: {stock_id}")
    print(f"日期範圍: {start_date} 至 {end_date}")
    print("-" * 60)
    
    try:
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
        print("\n" + "="*80)
        print(df_result.tail(10).to_string())
        print("="*80)
        print(f"\n(顯示最後 10 筆資料，共 {len(df_result)} 筆)")
        
        # 統計資訊
        print("\n📊 統計資訊:")
        print(f"平均收盤價: {df_result['收盤價'].mean():.2f}")
        print(f"最高價: {df_result['最高價'].max():.2f}")
        print(f"最低價: {df_result['最低價'].min():.2f}")
        print(f"總成交量: {df_result['成交量'].sum():,.0f}")
        print(f"最新交易日: {df_result.iloc[-1]['日期']} (收盤價: {df_result.iloc[-1]['收盤價']:.2f})")
        
        return df_result
        
    except ImportError:
        print("❌ 需要安裝 yfinance 模組")
        print("執行命令: pip install yfinance")
        return None
    except Exception as e:
        print(f"❌ 爬取失敗: {str(e)}")
        return None


def main():
    stock_id = '2330'  # 台積電
    
    print("="*80)
    print("台灣股市爬蟲程式 - 台積電 (2330)")
    print("="*80)
    
    # 獲取歷史交易資料
    result = get_twse_stock_data(
        stock_id=stock_id,
        start_date='2026-01-10',
        end_date='2026-02-25'
    )
    
    # 嘗試獲取即時行情
    realtime_data = get_realtime_stock_price(stock_id)
    
    if result is not None:
        # 存存為 CSV 檔案
        result.to_csv('stock_2330.csv', index=False, encoding='utf-8-sig')
        print("\n💾 資料已存存至 stock_2330.csv")
    
    print("\n" + "="*80)
    print("說明:")
    print("- 股市交易日為周一至周五 (不含國定假日)")
    print("- 如果沒有今天的資料，表示今天不是交易日")
    print("- 最新的交易資訊會顯示在上方")
    print("="*80)


if __name__ == "__main__":
    main()
