from dotenv import load_dotenv

from reasoner import reasoner, tools
from react_state import AgentState

load_dotenv()

def reason_node(state: AgentState):
    agent_outcome = reasoner.invoke(
        state["messages"]
    )
    return {
        "messages": [agent_outcome]
    }

    