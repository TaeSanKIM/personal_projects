from datetime import datetime, timedelta

import yfinance as yf
from pykrx import stock as krx

from .config import BASE_DATE, STOCKS


def _krx_price(ticker: str, from_date: str, days_forward: int = 10) -> float | None:
    """from_date부터 최대 days_forward일 이내의 첫 거래일 종가를 반환."""
    end = (datetime.strptime(from_date, "%Y%m%d") + timedelta(days=days_forward)).strftime("%Y%m%d")
    df = krx.get_market_ohlcv_by_date(from_date, end, ticker)
    if df.empty:
        return None
    return float(df.iloc[0]["종가"])


def _krx_recent_prices(ticker: str) -> tuple[float | None, float | None]:
    """(current_price, prev_price) 반환. API 1회 호출로 두 값을 모두 가져온다."""
    today = datetime.now()
    start = (today - timedelta(days=10)).strftime("%Y%m%d")
    end = today.strftime("%Y%m%d")
    df = krx.get_market_ohlcv_by_date(start, end, ticker)
    if df.empty:
        return None, None
    current = float(df.iloc[-1]["종가"])
    prev = float(df.iloc[-2]["종가"]) if len(df) >= 2 else None
    return current, prev


def _us_price(ticker: str, from_date: str, days_forward: int = 10) -> float | None:
    """from_date부터 최대 days_forward일 이내의 첫 거래일 종가를 반환."""
    start_dt = datetime.strptime(from_date, "%Y%m%d")
    end_dt = start_dt + timedelta(days=days_forward)
    hist = yf.Ticker(ticker).history(
        start=start_dt.strftime("%Y-%m-%d"),
        end=end_dt.strftime("%Y-%m-%d"),
    )
    if hist.empty:
        return None
    return float(hist.iloc[0]["Close"])


def _us_recent_prices(ticker: str) -> tuple[float | None, float | None]:
    """(current_price, prev_price) 반환. API 1회 호출로 두 값을 모두 가져온다."""
    hist = yf.Ticker(ticker).history(period="5d")
    if hist.empty:
        return None, None
    current = float(hist.iloc[-1]["Close"])
    prev = float(hist.iloc[-2]["Close"]) if len(hist) >= 2 else None
    return current, prev


def fetch_all() -> list[dict]:
    """모든 종목의 기준가·현재가·등락·전일대비 정보를 반환."""
    results = []

    for s in STOCKS:
        name, ticker, market = s["name"], s["ticker"], s["market"]
        try:
            if market == "KRX":
                base_price = _krx_price(ticker, BASE_DATE)
                current_price, prev_price = _krx_recent_prices(ticker)
                currency = "KRW"
            else:
                base_price = _us_price(ticker, BASE_DATE)
                current_price, prev_price = _us_recent_prices(ticker)
                currency = "USD"

            if base_price is None or current_price is None:
                raise ValueError("가격 데이터 없음")

            change = current_price - base_price
            change_pct = change / base_price * 100

            daily_change = None
            daily_change_pct = None
            if prev_price is not None:
                daily_change = current_price - prev_price
                daily_change_pct = daily_change / prev_price * 100

            results.append({
                "name": name,
                "ticker": ticker,
                "currency": currency,
                "base_price": base_price,
                "current_price": current_price,
                "change": change,
                "change_pct": change_pct,
                "daily_change": daily_change,
                "daily_change_pct": daily_change_pct,
            })
        except Exception as e:
            results.append({"name": name, "ticker": ticker, "error": str(e)})

    return results
