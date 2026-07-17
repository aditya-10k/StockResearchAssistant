from app.services.market.models import CompanySnapshot

def map_company_snapshot(ticker: str, info: dict) -> CompanySnapshot:
    """
    Maps raw market API info dictionary to the expanded CompanySnapshot Pydantic model.
    """
    if not isinstance(info, dict):
        info = {}

    # Helper function to safely cast float values
    def safe_float(value) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    # Helper function to safely cast integer values
    def safe_int(value) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    return CompanySnapshot(
        # Identity
        ticker=ticker.upper() if ticker else "UNKNOWN",
        company_name=info.get("longName"),
        short_name=info.get("shortName"),
        exchange=info.get("exchange"),
        quote_type=info.get("quoteType"),
        currency=info.get("currency"),

        # Business Profile
        sector=info.get("sector"),
        industry=info.get("industry"),
        country=info.get("country"),
        website=info.get("website"),
        employee_count=safe_int(info.get("fullTimeEmployees")),
        business_summary=info.get("longBusinessSummary"),

        # Price Information
        current_price=safe_float(info.get("currentPrice") or info.get("regularMarketPrice")),
        previous_close=safe_float(info.get("previousClose") or info.get("regularMarketPreviousClose")),
        open_price=safe_float(info.get("open") or info.get("regularMarketOpen")),
        day_high=safe_float(info.get("dayHigh") or info.get("regularMarketDayHigh")),
        day_low=safe_float(info.get("dayLow") or info.get("regularMarketDayLow")),
        fifty_two_week_high=safe_float(info.get("fiftyTwoWeekHigh")),
        fifty_two_week_low=safe_float(info.get("fiftyTwoWeekLow")),

        # Trading
        volume=safe_int(info.get("volume") or info.get("regularMarketVolume")),
        average_volume=safe_int(info.get("averageVolume") or info.get("averageDailyVolume10Day")),
        average_volume_10d=safe_int(info.get("averageVolume10days")),
        shares_outstanding=safe_int(info.get("sharesOutstanding")),
        float_shares=safe_int(info.get("floatShares")),

        # Market Size
        market_cap=safe_float(info.get("marketCap")),
        enterprise_value=safe_float(info.get("enterpriseValue")),

        # Valuation
        pe_ratio=safe_float(info.get("trailingPE")),
        forward_pe=safe_float(info.get("forwardPE")),
        peg_ratio=safe_float(info.get("pegRatio")),
        price_to_book=safe_float(info.get("priceToBook")),
        price_to_sales=safe_float(info.get("priceToSalesTrailing12Months")),
        enterprise_to_revenue=safe_float(info.get("enterpriseToRevenue")),
        enterprise_to_ebitda=safe_float(info.get("enterpriseToEbitda")),

        # Earnings
        eps=safe_float(info.get("trailingEps")),
        forward_eps=safe_float(info.get("forwardEps")),
        revenue_growth=safe_float(info.get("revenueGrowth")),
        earnings_growth=safe_float(info.get("earningsGrowth")),

        # Profitability
        gross_margin=safe_float(info.get("grossMargins")),
        operating_margin=safe_float(info.get("operatingMargins")),
        profit_margin=safe_float(info.get("profitMargins")),
        return_on_equity=safe_float(info.get("returnOnEquity")),
        return_on_assets=safe_float(info.get("returnOnAssets")),

        # Financial Health
        total_cash=safe_float(info.get("totalCash")),
        total_debt=safe_float(info.get("totalDebt")),
        debt_to_equity=safe_float(info.get("debtToEquity")),
        current_ratio=safe_float(info.get("currentRatio")),
        quick_ratio=safe_float(info.get("quickRatio")),
        free_cashflow=safe_float(info.get("freeCashflow")),

        # Dividend
        dividend_rate=safe_float(info.get("dividendRate")),
        dividend_yield=safe_float(info.get("dividendYield")),
        payout_ratio=safe_float(info.get("payoutRatio")),

        # Risk
        beta=safe_float(info.get("beta")),

        # Analyst Consensus
        recommendation=info.get("recommendationKey"),
        target_mean_price=safe_float(info.get("targetMeanPrice")),
        target_high_price=safe_float(info.get("targetHighPrice")),
        target_low_price=safe_float(info.get("targetLowPrice")),
    )
