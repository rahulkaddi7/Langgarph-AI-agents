from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import MessageGraph, END

from chains import revisor_chain, first_responder_chain
from execute_tool import execute_tool

graph = MessageGraph()
MAX_TOOL_ITERATIONS = 2

graph.add_node('RESPONDER', first_responder_chain)
graph.add_node('EXECUTE_TOOL', execute_tool)
graph.add_node('REVISOR', revisor_chain)

graph.add_edge('RESPONDER', 'EXECUTE_TOOL')
graph.add_edge('EXECUTE_TOOL', 'REVISOR')

def event_loop(state: List[BaseMessage]) -> str:
    tool_exec_counts = sum(isinstance(item, ToolMessage) for item in state)

    if tool_exec_counts > MAX_TOOL_ITERATIONS:
        return END
    return 'EXECUTE_TOOL'

graph.add_conditional_edges('REVISOR', event_loop)
graph.set_entry_point('RESPONDER')

app = graph.compile()

response = app.invoke('Write a blog on how ai helps in learning agentic ai')

final_response = response[-1].tool_calls[0]["args"]["answer"]
print(final_response)