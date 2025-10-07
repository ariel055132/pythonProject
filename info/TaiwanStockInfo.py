import argparse
import os
import sys
import pandas as pd
from typing import List, Dict
from datetime import datetime

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.requestUtils import request_get
from utils.csvUtils import save_to_csv

class TaiwanStockInfo:
    def __init__(self):
        self.base_url = 'https://api.finmindtrade.com/api/v4/data'

    def get_stock_deal_info(self, stock_id, start_date, end_date=None) -> List[Dict]:
        """股價日成交資訊 (https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html)
        :param stock_id: 股票代碼
        :param start_date: 開始日期
        :param end_date: 截止日期，不加則抓到前一個交易日
        :return data: 回應資料
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")

        parameter = {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": start_date,
            "end_date": end_date,
        }
        data = request_get(self.base_url, parameter)
        return data

def main():
    parser = argparse.ArgumentParser(description="Fetch Taiwan Stock Deal Info")
    parser.add_argument("stock_id", type=str, help="Stock ID (e.g 0050)")
    parser.add_argument("start_date", type=str, help="Start date (e.g 2021-09-13)")
    parser.add_argument("end_date", type=str, nargs="?", default=None, help="End date (YYYY-MM-DD, optional)")
    parser.add_argument("--output", type=str, default="stock_data.csv", help="Output CSV file name")
    args = parser.parse_args()

    stock_finmind = TaiwanStockInfo()
    stock_deal_info = stock_finmind.get_stock_deal_info(args.stock_id, args.start_date, args.end_date)
    data = pd.DataFrame(stock_deal_info)

    # Save the dataFrame to a CSV file
    save_to_csv(data, args.output)

if __name__ == "__main__":
    main()