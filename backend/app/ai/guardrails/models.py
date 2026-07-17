from enum import Enum
from pydantic import BaseModel

class GuardrailDecision(str , Enum) :

    ALLOW = 'allow'
    DENY = 'deny'
    CLARIFY = 'clarify'


class GuardRailResult(BaseModel):

    decision : GuardrailDecision 
    reason : str | None = None
    response : str | None = None