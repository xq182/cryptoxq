"""
=========================================================
* Powered by StudyQuant 
* author: Rudy
* wechat:studyquant88
=========================================================
* Product Page: https://studyquant.com
* Copyright 2021 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
import threading
from ahr import get_ahr999

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import ccxt
import socket

'''
    year (int|str) – 4-digit year
    month (int|str) – month (1-12)
    day (int|str) – day of the (1-31)
    week (int|str) – ISO week (1-53)
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    hour (int|str) – hour (0-23)
    minute (int|str) – minute (0-59)
    second (int|str) – second (0-59)
    
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
    
    *    any    Fire on every value
    */a    any    Fire every a values, starting from the minimum
    a-b    any    Fire on any value within the a-b range (a must be smaller than b)
    a-b/c    any    Fire every c values within the a-b range
    xth y    day    Fire on the x -th occurrence of weekday y within the month
    last x    day    Fire on the last occurrence of weekday x within the month
    last    day    Fire on the last day within the month
    x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
'''

#

# 'proxies': {
#     'http': '127.0.0.1:7897',
#     'https': '127.0.0.1:7897'
# }

exchange = ccxt.binance(

    {
        'apiKey': 'g0G9maOBYMbcgqc8vRAohK5q7j1dSRCu5wIkl5HoUSoWI7hopOeRr7p9N8Jczgfi',
        'secret': 'tfLZcHoKlwycpmbL8TLk7sXxdwV9Ho2pUcWB1FDLalsiVbeo9Qe2oYJmkTWPUs23',
        'timeout': 30000,
        'enableRateLimit': True
    }
)


# 模仿购买股票函数
def buy(symbol, amount, cut):
    ticker = exchange.fetch_ticker(symbol)
    sell_price = ticker['ask'] - cut
    number = amount / sell_price
    # 开始下单购买 B
    order_info = exchange.create_limit_buy_order(symbol, number, sell_price)
    print(
        f"buy_success {symbol} @{sell_price} Amount:{amount} number:{number} id:{order_info['id']} time:{datetime.now()}",
        flush=True)


#  nohup python  buy.py >xq.log&
# ps aux | grep buy.py
# kill - 9 73465

# scheduler.add_job(buy, 'cron', second='*/59', args=['FDUSD/USDT', 6,0.0001])


def compute_buy_amount():
    _, _, _, ahr999 = get_ahr999()
    amount = (1.2 - ahr999) * 250
    print(f"search {datetime.now()} ahr999={ahr999:.4f}, buy amount={amount:.4f}", flush=True)
    return amount, ahr999


def buy_btc():
    try:
        # 调用另一个文件的 get_ahr999
        amount, ahr999 = compute_buy_amount()
        buy("BTC/FDUSD", amount, 30)

    except Exception as e:
        print(f"buy_fail {datetime.now()} 出现异常: {e}", flush=True)


def main():
    job_defaults = {
        'max_instances': 30,
        'misfire_grace_time': None
    }
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai', job_defaults=job_defaults)
    scheduler.add_job(buy_btc, 'cron', hour='*')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()

    while True:
        time.sleep(1)
