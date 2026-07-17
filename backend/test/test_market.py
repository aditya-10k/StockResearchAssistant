from app.services.market.service import MarketService

service = MarketService()

snapshot = service.get_company_snapshot("NVDA")
print(snapshot.model_dump_json(indent=2))