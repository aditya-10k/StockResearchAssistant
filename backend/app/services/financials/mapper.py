import json

from pandas import DataFrame

from app.services.financials.models import FinancialsSnapshot


def _serialize_frame(frame: DataFrame) -> dict:
    return json.loads(frame.to_json(orient="split", date_format="iso"))


def map_financials(ticker: str, financials: dict[str, DataFrame]) -> FinancialsSnapshot:
    return FinancialsSnapshot(
        ticker=ticker.upper(),
        annual_income_statement=_serialize_frame(financials["annual_income_statement"]),
        quarterly_income_statement=_serialize_frame(financials["quarterly_income_statement"]),
        annual_balance_sheet=_serialize_frame(financials["annual_balance_sheet"]),
        quarterly_balance_sheet=_serialize_frame(financials["quarterly_balance_sheet"]),
        annual_cash_flow=_serialize_frame(financials["annual_cash_flow"]),
        quarterly_cash_flow=_serialize_frame(financials["quarterly_cash_flow"]),
    )
