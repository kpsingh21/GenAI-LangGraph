from langgraph.graph import StateGraph , START, END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage , HumanMessage
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
# this store the data in ram
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

# need to define checkpointer obj of MemorySaver class
checkpointer = MemorySaver()

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

# res = chatbot.invoke() instead of this we will use chatbot.stream()


# codde to implememt stream

# config = { 'configurable': {'thread_id': 1}}
# for message_chunk, metadata in chatbot.stream(
#     {'messages': [HumanMessage(content='what is the recipe to make pasta')]},
#     config=config,
#     stream_mode='messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content,end=" ",flush=True)

# print(type(stream))







