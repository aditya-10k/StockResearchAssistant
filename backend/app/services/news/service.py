import yfinance as yf

class NewsService :

    def get_company_news(self , ticker: str) :

        stock = yf.Ticker(ticker)
        return stock.news