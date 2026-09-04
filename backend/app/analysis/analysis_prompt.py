import json
from typing import Any

from app.services.market.models import CompanySnapshot


def _format_financials_summary(fin_data: Any) -> str:
    if not fin_data:
        return "None"
    d = fin_data.model_dump() if hasattr(fin_data, "model_dump") else fin_data
    if not isinstance(d, dict):
        return str(fin_data)[:300]

    lines = []
    key_items = [
        "Total Revenue",
        "Operating Revenue",
        "Net Income",
        "Normalized EBITDA",
        "Operating Cash Flow",
        "Free Cash Flow",
        "Total Debt",
        "Cash And Cash Equivalents",
    ]

    for report_name in ["annual_income_statement", "annual_balance_sheet", "annual_cash_flow"]:
        rep = d.get(report_name)
        if rep and isinstance(rep, dict):
            idx = rep.get("index", [])
            data = rep.get("data", [])
            cols = rep.get("columns", [])
            latest_col = cols[0][:10] if cols else ""
            for item in key_items:
                if item in idx:
                    i = idx.index(item)
                    val = data[i][0] if data and len(data) > i and data[i] else None
                    if val is not None:
                        if isinstance(val, (int, float)):
                            lines.append(f"  {item} ({latest_col}): {val:,.0f}")
                        else:
                            lines.append(f"  {item} ({latest_col}): {val}")
    return "\n".join(lines) if lines else "Key financial statement items not available"


def _format_earnings_summary(earnings_data: Any) -> str:
    if not earnings_data:
        return "None"
    d = earnings_data.model_dump() if hasattr(earnings_data, "model_dump") else earnings_data
    if not isinstance(d, dict):
        return str(earnings_data)[:300]
    ed = d.get("earnings_dates")
    if not ed or not isinstance(ed, dict):
        return "None"
    index = ed.get("index", [])[:4]
    rows = ed.get("data", [])[:4]
    lines = []
    for date, row in zip(index, rows):
        lines.append(f"  Date: {date[:10]} | EPS Est: {row[0]} | Reported EPS: {row[1]} | Surprise: {row[2]}%")
    return "\n".join(lines) if lines else "None"


def build_analysis_prompt(
    query: str,
    market_data: list[CompanySnapshot],
    news_data: dict[str, list[dict[str, Any]]],
    financials_data: dict[str, Any],
    price_history_data: dict[str, Any],
    calendar_data: dict[str, Any],
    holders_data: dict[str, Any],
    recommendations_data: dict[str, Any],
    earnings_data: dict[str, Any],
) -> str:

    prompt = f"""User Query:
{query}

==================================================
MARKET DATA & VALUATION MULTIPLES
==================================================
"""

    for company in market_data:
        prompt += f"""Ticker: {company.ticker} ({company.company_name})
Sector: {company.sector} | Industry: {company.industry}
Current Price: {company.current_price} | Market Cap: {company.market_cap}
Trailing P/E: {company.pe_ratio} | Forward P/E: {company.forward_pe}
Revenue Growth: {company.revenue_growth} | Earnings Growth: {company.earnings_growth}
Return on Equity (ROE): {company.return_on_equity} | Profit Margin: {company.profit_margin}
Debt to Equity: {company.debt_to_equity}
Consensus Target Price: {company.target_mean_price} | Recommendation: {company.recommendation}
--------------------------------------------------
"""

    prompt += """
==================================================
LATEST NEWS
==================================================
"""
    for ticker, articles in news_data.items():
        prompt += f"Ticker: {ticker}\n"
        if not articles:
            prompt += "  No recent news.\n"
            continue
        for article in articles[:3]:
            content = article.get("content", {})
            title = content.get("title", "No title")
            summary = content.get("summary", "")
            if summary and len(summary) > 180:
                summary = summary[:180] + "..."
            pub = content.get("provider", {}).get("displayName", "News")
            prompt += f"  - [{pub}] {title}: {summary}\n"

    prompt += """
==================================================
KEY FINANCIAL STATEMENTS SUMMARY
==================================================
"""
    for ticker, fin in financials_data.items():
        prompt += f"Ticker: {ticker}:\n{_format_financials_summary(fin)}\n"

    prompt += """
==================================================
QUARTERLY EARNINGS HISTORY
==================================================
"""
    for ticker, earn in earnings_data.items():
        prompt += f"Ticker: {ticker}:\n{_format_earnings_summary(earn)}\n"

    return prompt
