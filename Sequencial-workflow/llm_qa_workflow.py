from langgraph.graph import StateGraph , START , END
# from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from typing import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()


#model
# model =  ChatOpenAI()

#create a state
class LLMState(TypedDict):
    question: str
    answer: str


def llm_qa(state: LLMState ) -> LLMState:

    #extract the question from state:
    que = state['question']

    #form a prompt
    prompt = f'Answer the following question {que}'

    #ask this que to LLM
    ans = model.invoke(prompt).content

    #update the answer to llm
    state['answer']=answer

    return state


    

#create a graph 

graph = StateGraph(LLMState)

#add node

graph.add_node('llm_qa',llm_qa)

#add edge

graph.add_edge(START, 'llm_qa')
graph.add_edge('llm_qa', END)




#compile graph

workflow = graph.compile()

res = workflow.invoke({'question': 'what is the capital of india'})



