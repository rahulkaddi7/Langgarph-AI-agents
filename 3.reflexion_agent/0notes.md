### responder flow

- create template using the ChatPromptTemplate(can use f"{variable}" too, but complex)
- bind tool(pyndactic schema) and make it neccessary for the llm to use to output in required format
- invoke llm
- the answer is again checked by pyndatic_parser parser(bind schema with that)

### comments

1. tool_choice - forces llm to use that tool no matter what

2. what does | ('pipe') do? this is LCE Langauage, x|y -> output of x goes to y

3. point number 1,2,3 in actor_prompt_template -> response: , critique: , search:

4. partial-> prefill before even invoking
