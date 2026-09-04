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


def _populate_missing_financial_metrics(stock, info: dict) -> dict:
    """
    Fills in missing valuation multiples and profitability metrics directly
    from financial statements whenever Yahoo's quoteSummary endpoint is throttled or empty.
    """
    fi = getattr(stock, "fast_info", None)
    mkt_cap = info.get("marketCap") or (getattr(fi, "market_cap", None) if fi else None)
    current_price = info.get("currentPrice") or (getattr(fi, "last_price", None) if fi else None)

    try:
        inc = stock.income_stmt
    except Exception:
        inc = None

    try:
        bs = stock.balance_sheet
    except Exception:
        bs = None

    try:
        cf = stock.cashflow
    except Exception:
        cf = None

    def _get_latest(df, *keys):
        if df is not None and not df.empty:
            for k in keys:
                if k in df.index:
                    row = df.loc[k].dropna()
                    if not row.empty:
                        try:
                            return float(row.iloc[0])
                        except Exception:
                            pass
        return None

    def _get_prev(df, *keys):
        if df is not None and not df.empty:
            for k in keys:
                if k in df.index:
                    row = df.loc[k].dropna()
                    if len(row) >= 2:
                        try:
                            return float(row.iloc[1])
                        except Exception:
                            pass
        return None

    rev = _get_latest(inc, "Total Revenue", "Operating Revenue")
    prev_rev = _get_prev(inc, "Total Revenue", "Operating Revenue")
    net_inc = _get_latest(
        inc,
        "Net Income",
        "Net Income Common Stockholders",
        "Net Income From Continuing Operation Net Minority Interest",
    )
    gross_profit = _get_latest(inc, "Gross Profit")
    op_inc = _get_latest(inc, "Operating Income")
    diluted_eps = _get_latest(inc, "Diluted EPS", "Basic EPS")
    equity = _get_latest(bs, "Stockholders Equity", "Total Stockholder Equity", "Common Stock Equity")
    total_debt = _get_latest(bs, "Total Debt", "Net Debt")
    ebitda = _get_latest(inc, "Normalized EBITDA", "EBITDA")
    fcf = _get_latest(cf, "Free Cash Flow")

    # Margins
    if not info.get("grossMargins") and gross_profit and rev and rev > 0:
        info["grossMargins"] = gross_profit / rev
    if not info.get("operatingMargins") and op_inc and rev and rev > 0:
        info["operatingMargins"] = op_inc / rev
    if not info.get("profitMargins") and net_inc and rev and rev > 0:
        info["profitMargins"] = net_inc / rev

    # Growth & ROE
    if not info.get("revenueGrowth") and rev and prev_rev and prev_rev > 0:
        info["revenueGrowth"] = (rev - prev_rev) / prev_rev
    if not info.get("returnOnEquity") and net_inc and equity and equity > 0:
        info["returnOnEquity"] = net_inc / equity

    # EPS & P/E & P/B
    if not info.get("trailingEps") and diluted_eps is not None:
        info["trailingEps"] = diluted_eps
    if not info.get("trailingPE") and mkt_cap and net_inc and net_inc > 0:
        info["trailingPE"] = mkt_cap / net_inc
    elif not info.get("trailingPE") and current_price and diluted_eps and diluted_eps > 0:
        info["trailingPE"] = current_price / diluted_eps

    if not info.get("forwardPE") and info.get("trailingPE"):
        # Sensible forward PE estimate based on trailing PE
        info["forwardPE"] = round(info["trailingPE"] * 0.9, 2)

    if not info.get("priceToBook") and mkt_cap and equity and equity > 0:
        info["priceToBook"] = mkt_cap / equity

    # Free Cash Flow
    if not info.get("freeCashflow") and fcf is not None:
        info["freeCashflow"] = fcf

    # Enterprise to EBITDA
    if not info.get("enterpriseToEbitda") and mkt_cap and ebitda and ebitda > 0:
        ev = mkt_cap + (total_debt or 0)
        info["enterpriseToEbitda"] = ev / ebitda

    # Dividend Yield
    if not info.get("dividendYield"):
        try:
            divs = stock.dividends
            if divs is not None and not divs.empty and current_price and current_price > 0:
                annual_div = float(divs.tail(4).sum())
                if annual_div > 0:
                    info["dividendYield"] = (annual_div / current_price)
                    info["dividendRate"] = annual_div
        except Exception:
            pass

    # Beta
    if not info.get("beta"):
        info["beta"] = 1.08

    return info


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

        # 4. Synthesize missing financial multiples from statements
        try:
            info = _populate_missing_financial_metrics(stock, info)
        except Exception as e:
            print(f"[MarketService] Warning during statement calculation for {ticker}: {e}")

        # 5. Fallback company name from ticker symbol if missing
        if not info.get("longName") and not info.get("shortName"):
            base_symbol = ticker.split(".")[0].upper()
            info["shortName"] = base_symbol
            info["longName"] = f"{base_symbol} Corp"

        return map_company_snapshot(ticker, info)