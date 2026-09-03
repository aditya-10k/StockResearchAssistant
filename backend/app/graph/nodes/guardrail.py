from app.graph.state import GraphState
from app.ai.guardrails.service import GuardrailService

guardrail_service = GuardrailService()

def guardrail_node(state : GraphState) :
    query = state['query']
    if state.get('chat_history'):
        history_str = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in state['chat_history']])
        query = f"Previous Conversation Context:\n{history_str}\n\nCurrent Query:\n{query}"

    result = guardrail_service.validate(query)
    print(result)


    return{
        "guardrail" : result
    }