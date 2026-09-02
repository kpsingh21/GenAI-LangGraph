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


# Both HumanMessage and AIMessage are types of BaseMessage.
# Annotated allows you to attach additional information/metadata to a type.
# Annotated[type, metadata]

#the state will replace the value with new value so we will use reducer fun

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

# intial_state = {
#     'messages': [HumanMessage(content='what is the capital of india')]
# }

# result = chatbot.invoke(intial_state)['messages'][-1].content
# print(result)


#code to fill like chat bot

# thread means the seesions
thread_id = '1'
while True:
    user_message = input('Type here: ')
    if user_message.strip().lower() in ['exit','quit','bye']:
        break


#  we need to define this config variable
    config = { 'configurable': {'thread_id': thread_id}}
    response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)

    print('AI:',response['messages'][-1].content)

    # 
    print(chatbot.get_state(config=config))

# till here we are passing the previous history also but chatbot not able to use it
# because here we are invokeing the llm , multiple time generally when we invoke and it went til end the state get reset
# so now here came the concept of persistance
# in which we will store the state either in database or RAM








