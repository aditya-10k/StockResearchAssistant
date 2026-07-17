from pydantic import BaseModel


class AnalysisResult(BaseModel):

    summary: str

    investment_thesis: str

    strengths: list[str]

    risks: list[str]

    valuation: str

    conclusion: str