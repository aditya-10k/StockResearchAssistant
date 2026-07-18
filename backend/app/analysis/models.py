from pydantic import BaseModel


class AnalysisResult(BaseModel):

    direct_answer: str

    summary: str

    investment_thesis: str

    strengths: list[str]

    risks: list[str]

    valuation: str

    conclusion: str
