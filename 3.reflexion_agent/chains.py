from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import datetime

from schema import  AnswerQuestion, ReviseAnswer

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

# =============== RESPONDER SECTION =========================

# Actor Agent Prompt
#4,5 -> explanation in notes.md
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are expert AI researcher.
            Current time: {time}

            1. {first_instruction}
            2. Reflect and critique your answer. Be severe to maximize improvement.
            3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time= lambda: datetime.datetime.now().isoformat()
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction = 'Provide a detailed ~250 words answer'
)

tools = [AnswerQuestion]

#1,2 -> explanation in notes.md
first_responder_chain = first_responder_prompt_template | llm.bind_tools(
                        tools, tool_choice='AnswerQuestion') 

validator = PydanticToolsParser(tools=[AnswerQuestion])

# =============== REVISOR SECTION ==============================
revise_instructions = """Revise your previous answer using the new
information.

    - You should use the previous critique to add important information to
      your answer.
        - You MUST include numerical citations in your revised answer to
          ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which
          does not count towards the word limit). In form of:
              - [1] https://example.com
              - [2] https://example.com

    - You should use the previous critique to remove superfluous
      information from your answer and make SURE it is not more than 250
      words.
"""

revisor_prompt_template = actor_prompt_template.partial(
    first_instruction = revise_instructions
)

revisor_chain = revisor_prompt_template | llm.bind_tools(
                    tools=[ReviseAnswer], tool_choice='ReviseAnswer') 