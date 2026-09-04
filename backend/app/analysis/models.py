from typing import Any
from pydantic import BaseModel, model_validator


class AnalysisResult(BaseModel):
    direct_answer: str = ""
    summary: str = ""
    investment_thesis: str = ""
    strengths: list[str] = []
    risks: list[str] = []
    valuation: str = ""
    conclusion: str = ""

    @model_validator(mode='before')
    @classmethod
    def normalize_analysis(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get('direct_answer'):
                data['direct_answer'] = data.get('direct_verdict', data.get('verdict', ''))
            if not data.get('investment_thesis'):
                data['investment_thesis'] = data.get('thesis', '')
        return data

