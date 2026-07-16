from app.ai.planner.planner_service import PlannerService

planner = PlannerService()

plan = planner.create_plan(
    "Analyse IDFCFIRSTB"
)

print("plan")
print(plan)