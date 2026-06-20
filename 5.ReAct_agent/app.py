from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from nodes import reason_node
from react_state import AgentState
from reasoner import tools

REASON_NODE = "reason_node"
ACT_NODE = "tools"

graph = StateGraph(AgentState)

graph.add_node(REASON_NODE, reason_node)
graph.add_node(ACT_NODE, ToolNode(tools))

graph.add_edge(ACT_NODE, REASON_NODE)
graph.add_conditional_edges(REASON_NODE, tools_condition)

graph.set_entry_point(REASON_NODE)

app= graph.compile()

result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="How many days ago was the last SpaceX launch?"
            )
        ]
    }
)

last_message = result["messages"][-1]

# print(last_message)
# print(type(last_message.content))

last_message = result["messages"][-1]

if isinstance(last_message.content, list):
    print(last_message.content[0]["text"])
else:
    print(last_message.content)