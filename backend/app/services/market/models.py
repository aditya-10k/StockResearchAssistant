from pydantic import BaseModel


class CompanySnapshot(BaseModel):

    # ------------------------
    # Identity
    # ------------------------
    ticker: str
    company_name: str | None = None
    short_name: str | None = None
    exchange: str | None = None
    quote_type: str | None = None
    currency: str | None = None

    # ------------------------
    # Business Profile
    # ------------------------
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    website: str | None = None
    employee_count: int | None = None
    business_summary: str | None = None

    # ------------------------
    # Price Information
    # ------------------------
    current_price: float | None = None
    previous_close: float | None = None
    open_price: float | None = None
    day_high: float | None = None
    day_low: float | None = None

    fifty_two_week_high: float | None = None
    fifty_two_week_low: float | None = None

    # ------------------------
    # Trading
    # ------------------------
    volume: int | None = None
    average_volume: int | None = None
    average_volume_10d: int | None = None

    shares_outstanding: int | None = None
    float_shares: int | None = None

    # ------------------------
    # Market Size
    # ------------------------
    market_cap: float | None = None
    enterprise_value: float | None = None

    # ------------------------
    # Valuation
    # ------------------------
    pe_ratio: float | None = None
    forward_pe: float | None = None
    peg_ratio: float | None = None

    price_to_book: float | None = None
    price_to_sales: float | None = None

    enterprise_to_revenue: float | None = None
    enterprise_to_ebitda: float | None = None

    # ------------------------
    # Earnings
    # ------------------------
    eps: float | None = None
    forward_eps: float | None = None

    revenue_growth: float | None = None
    earnings_growth: float | None = None

    # ------------------------
    # Profitability
    # ------------------------
    gross_margin: float | None = None
    operating_margin: float | None = None
    profit_margin: float | None = None

    return_on_equity: float | None = None
    return_on_assets: float | None = None

    # ------------------------
    # Financial Health
    # ------------------------
    total_cash: float | None = None
    total_debt: float | None = None

    debt_to_equity: float | None = None

    current_ratio: float | None = None
    quick_ratio: float | None = None

    free_cashflow: float | None = None

    # ------------------------
    # Dividend
    # ------------------------
    dividend_rate: float | None = None
    dividend_yield: float | None = None
    payout_ratio: float | None = None

    # ------------------------
    # Risk
    # ------------------------
    beta: float | None = None

    # ------------------------
    # Analyst Consensus
    # ------------------------
    recommendation: str | None = None

    target_mean_price: float | None = None
    target_high_price: float | None = None
    target_low_price: float | None = None