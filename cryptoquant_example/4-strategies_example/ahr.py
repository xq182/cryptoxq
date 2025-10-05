import requests
import time
import math
import statistics
import json

API_HOST = "https://api.coingecko.com/api/v3"

# 代理配置（改成你的）
# PROXIES = {
#     "http": "http://127.0.0.1:7897",
#     "https": "http://127.0.0.1:7897",
# }

def coingecko_price(coin_id, vs_currency="usd"):
    url = f"{API_HOST}/simple/price"
    params = {"ids": coin_id, "vs_currencies": vs_currency}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def coingecko_market_chart_range(coin_id, vs_currency, from_ts, to_ts):
    url = f"{API_HOST}/coins/{coin_id}/market_chart/range"
    params = {
        "vs_currency": vs_currency,
        "from": from_ts,
        "to": to_ts,
    }
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()

def get_ahr999(offset=0):
    now = int(time.time())
    before = now - 24 * 200 * 60 * 60- offset * 24 * 60 * 60

    # 获取价格序列
    data = coingecko_market_chart_range("bitcoin", "usd", before, now)
    prices = [p[1] for p in data.get("prices", [])]  # 取出价格部分

    # 调和平均值
    avg = statistics.harmonic_mean(prices)

    # 当前价格
    js1 = coingecko_price("bitcoin", "usd")
    price = js1["bitcoin"]["usd"]

    # 计算 logprice
    bornday = (now - 1230940800) // (24 * 60 * 60)
    logprice = math.pow(10, 5.84 * math.log10(bornday) - 17.01)

    # 计算 ahr999
    ahr999 = round((price / avg) * (price / logprice), 3)

    return price, avg, logprice, ahr999

