from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
import datetime

load_dotenv()

llm = ChatGoogleGenerativeAI(model= 'gemini-3.1-flash-lite')
search_tool = TavilySearchResults(search_depth = "basic")

@tool
def get_current_time(format: str= "%Y-%m-%d %H:%M:%S"):
    """ RETURNS CURRENT DATE AND TIME IN SPECIFIC FORMAT """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

tools = [search_tool, get_current_time]

reasoner = llm.bind_tools(tools=tools)

