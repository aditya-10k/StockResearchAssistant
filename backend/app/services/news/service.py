import yfinance as yf
from typing import Any

class NewsService:

    def get_company_news(self, ticker: str) -> list[dict[str, Any]]:
        stock = yf.Ticker(ticker)
        raw_news = stock.news or []
        normalized = []

        for item in raw_news:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if isinstance(content, dict):
                title = content.get("title") or item.get("title") or "Market Update"
                provider = content.get("provider")
                pub = provider.get("displayName") if isinstance(provider, dict) else None
                source = pub or item.get("publisher") or "Yahoo Finance"
                link_obj = content.get("canonicalUrl") or content.get("clickThroughUrl") or {}
                link = link_obj.get("url") if isinstance(link_obj, dict) else item.get("link", "")
                summary = content.get("summary") or item.get("summary", "")
                pub_date = content.get("pubDate") or item.get("providerPublishTime", "")
            else:
                title = item.get("title") or item.get("headline") or "Market Update"
                source = item.get("publisher") or item.get("source") or "Yahoo Finance"
                link = item.get("link", "")
                summary = item.get("summary", "")
                pub_date = str(item.get("providerPublishTime", ""))

            normalized.append({
                "title": title,
                "publisher": source,
                "link": link,
                "summary": summary,
                "pubDate": pub_date,
                # Retain raw content map for backward compatibility
                "content": content if isinstance(content, dict) else {},
            })

        return normalized