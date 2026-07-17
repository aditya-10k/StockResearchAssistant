from app.analysis.service import AnalysisService
from app.ai.planner.planner_service import PlannerService
from app.services.market.service import MarketService

planner = PlannerService()
market = MarketService()
analysis = AnalysisService()

query = "Compare amazon and nvdia"

plan = planner.create_plan(query)

snapshots = []

for company in plan.entities:
    snapshots.append(
        market.get_company_snapshot(company.ticker)
    )

result = analysis.analyze(
    query=query,
    execution_plan=plan,
    market_data=snapshots,
)

print(result.model_dump_json(indent=4))
