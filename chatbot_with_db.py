from langgraph.graph import StateGraph , START, END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage , HumanMessage
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
# from langgraph.checkpoint.memory import 
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]


#add db
conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)
# check_same_thread false means we are going to use same database for diff diff threads

#checkpointer
# checkpointer = MemorySaver() in RAM storage

checkpointer = SqliteSaver(conn=conn)

# add graph
graph = StateGraph(ChatState)

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.8-2.4T-A95B",
    task="conversational",
    max_new_tokens=200,
    temperature=0,
)

model = ChatHuggingFace(llm=llm)

def chat_node(state: ChatState):
    #take user query from state
    msg = state['messages']
    #send to llm
    res = model.invoke(msg)
    #response store state
    return {'messages': [res]}
#add nodes
graph.add_node('chat_node',chat_node)

#add edge
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

# here we  need to pass checkpointer
chatbot = graph.compile(checkpointer=checkpointer)

# none means all the checkpointer irrespective of thread id


def retrive_all_threads():
    all_threads = set()  # we used set here so that it help to store unique.
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)