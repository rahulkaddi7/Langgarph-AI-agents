from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_community.tools import TavilySearchResults
from typing import List
import json

tavily_tool = TavilySearchResults(max_reslults=5)

def execute_tool(state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message = state[-1]

    if not hasattr(last_ai_message, 'tool_calls') or not last_ai_message.tool_calls:
        return []
    
    tool_message = []

    for tool_call in last_ai_message.tool_calls:
        if tool_call['name'] in ["AnswerQuestion", "ReviseAnswer"]:
            call_id = tool_call['id']
            search_queries = tool_call['args'].get('search_queries')

            query_result = {}
            for query in search_queries:
                result = tavily_tool.invoke(query)
                query_result[query] = result

            tool_message.append(
                ToolMessage(
                    content=json.dumps(query_result),
                    tool_call_id = call_id 
                )
            )
    return tool_message
    
# ====================== HOW DOES state look like: ===============================
# test_state = [
#     HumanMessage(
#         content="Write about how small business can leverage AI to grow"
#     ),
#     AIMessage(
#         content="", 
#         tool_calls=[
#             {
#                 "name": "AnswerQuestion",
#                 "args": {
#                     'answer': '', 
#                     'search_queries': [
#                             'AI tools for small business', 
#                             'AI in small business marketing', 
#                             'AI automation for small business'
#                     ], 
#                     'reflection': {
#                         'missing': '', 
#                         'superfluous': ''
#                     }
#                 },
#                 "id": "call_KpYHichFFEmLitHFvFhKy1Ra",
#             }
#         ],
#     )
# ]