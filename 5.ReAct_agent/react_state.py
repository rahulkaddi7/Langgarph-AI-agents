from typing import Annotated, TypedDict, Union
import operator

from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
