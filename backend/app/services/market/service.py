import yfinance as yf
import requests
from app.services.market.mapper import map_company_snapshot

# Shared persistent session with real desktop browser headers to bypass datacenter IP restrictions
_session = requests.Session()
_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
})


class MarketService:

    def get_company_snapshot(self, ticker: str):
        try:
            stock = yf.Ticker(ticker, session=_session)
        except Exception:
            stock = yf.Ticker(ticker)

        # 1. Attempt to fetch full info dictionary
        info = {}
        try:
            raw_info = stock.info
            if isinstance(raw_info, dict):
                info = dict(raw_info)
        except Exception:
            info = {}

        # 2. Resilient fast_info merge (uses Yahoo's chart endpoint which never blocks)
        try:
            fi = stock.fast_info
            if fi:
                def _get(attr):
                    try:
                        return getattr(fi, attr, None)
                    except Exception:
                        return None

                if not info.get("currentPrice"):
                    info["currentPrice"] = _get("last_price")
                if not info.get("previousClose"):
                    info["previousClose"] = _get("previous_close")
                if not info.get("fiftyTwoWeekHigh"):
                    info["fiftyTwoWeekHigh"] = _get("year_high")
                if not info.get("fiftyTwoWeekLow"):
                    info["fiftyTwoWeekLow"] = _get("year_low")
                if not info.get("marketCap"):
                    info["marketCap"] = _get("market_cap")
                if not info.get("open"):
                    info["open"] = _get("open")
                if not info.get("dayHigh"):
                    info["dayHigh"] = _get("day_high")
                if not info.get("dayLow"):
                    info["dayLow"] = _get("day_low")
                if not info.get("exchange"):
                    info["exchange"] = _get("exchange")
                if not info.get("currency"):
                    info["currency"] = _get("currency")
        except Exception:
            pass

        # 3. History fallback for current & previous close price if still missing
        if not info.get("currentPrice"):
            try:
                hist = stock.history(period="2d")
                if not hist.empty and "Close" in hist:
                    closes = hist["Close"].dropna()
                    if len(closes) >= 1:
                        info["currentPrice"] = float(closes.iloc[-1])
                    if len(closes) >= 2:
                        info["previousClose"] = float(closes.iloc[-2])
            except Exception:
                pass

        # 4. Fallback company name from ticker symbol if missing
        if not info.get("longName") and not info.get("shortName"):
            base_symbol = ticker.split(".")[0].upper()
            info["shortName"] = base_symbol
            info["longName"] = f"{base_symbol} Corp"

        return map_company_snapshot(ticker, info)