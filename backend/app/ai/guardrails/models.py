from enum import Enum
from typing import Any
from pydantic import BaseModel, model_validator

class GuardrailDecision(str , Enum) :
    ALLOW = 'allow'
    DENY = 'deny'
    CLARIFY = 'clarify'


class GuardRailResult(BaseModel):
    decision : GuardrailDecision = GuardrailDecision.ALLOW
    reason : str | None = None
    response : str | None = None

    @model_validator(mode='before')
    @classmethod
    def map_status_to_decision(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'status' in data and 'decision' not in data:
                data['decision'] = data['status']
        return data