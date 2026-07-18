import json
from typing import Any

from app.services.market.models import CompanySnapshot


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

    prompt = f"""
User Query:
{query}

==================================================
MARKET DATA
==================================================
"""

    for company in market_data:

        prompt += f"""
Ticker: {company.ticker}
Company: {company.company_name}

Sector: {company.sector}
Industry: {company.industry}

Current Price: {company.current_price}
Market Cap: {company.market_cap}

PE Ratio: {company.pe_ratio}
Forward PE: {company.forward_pe}

Revenue Growth: {company.revenue_growth}
Earnings Growth: {company.earnings_growth}

ROE: {company.return_on_equity}
Profit Margin: {company.profit_margin}

Debt To Equity: {company.debt_to_equity}

Analyst Recommendation: {company.recommendation}
Target Price: {company.target_mean_price}

--------------------------------------------------
"""

    prompt += """

==================================================
LATEST NEWS
==================================================
"""

    for ticker, articles in news_data.items():

        prompt += f"\nTicker: {ticker}\n"

        if not articles:
            prompt += "No recent news available.\n"
            continue

        for article in articles[:5]:

            content = article.get("content", {})

            prompt += f"""
Title: {content.get("title")}

Summary: {content.get("summary")}

Publisher: {content.get("provider", {}).get("displayName")}

Published: {content.get("pubDate")}

URL: {content.get("canonicalUrl", {}).get("url")}

-----------------------------
"""

    for title, data in (
        ("FINANCIALS", financials_data),
        ("PRICE HISTORY", price_history_data),
        ("CALENDAR", calendar_data),
        ("HOLDERS", holders_data),
        ("RECOMMENDATIONS", recommendations_data),
        ("EARNINGS", earnings_data),
    ):
        if not data:
            continue

        prompt += f"\n==================================================\n{title}\n==================================================\n"
        for ticker, result in data.items():
            serialized = result.model_dump() if hasattr(result, "model_dump") else result
            prompt += f"\nTicker: {ticker}\n{json.dumps(serialized, default=str)}\n"

    return prompt
