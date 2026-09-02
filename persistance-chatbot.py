
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.8-2.4T-A95B",
    task="conversational",
    max_new_tokens=200,
    temperature=0,
)

model = ChatHuggingFace(llm=llm)


class JokeState(TypedDict):

    topic: str
    joke: str
    explanation: str


def generate_joke(state: JokeState):

    prompt = f'generate a joke on the topic {state["topic"]}'
    response = model.invoke(prompt).content

    return {'joke': response}


def generate_explanation(state: JokeState):

    prompt = f'write an explanation for the joke - {state["joke"]}'
    response = model.invoke(prompt).content

    return {'explanation': response}


graph = StateGraph(JokeState)

graph.add_node('generate_joke', generate_joke)
graph.add_node('generate_explanation', generate_explanation)

graph.add_edge(START, 'generate_joke')
graph.add_edge('generate_joke', 'generate_explanation')
graph.add_edge('generate_explanation', END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer=checkpointer)

config1 = {"configurable": {"thread_id": "1"}}
result = workflow.invoke({'topic':'pizza'}, config=config1)


#this will give you final value of state
workflow.get_state(config1)


#this will give you history
list(workflow.get_state_history(config1))


#Time Travel
# with the help of checkpoint id we can go to that particular node
workflow.get_state({"configurable": {"thread_id": "1"}}, "checkpoint_id":"idfacecdfa")

# and to invoke from that particular step do this
workflow.invoke(None , {"configurable": {"thread_id": "1"}}, "checkpoint_id":"idfacecdfa")

#we can update state also
workflow.update_state({"configurable": {"thread_id": "1", "checkpoint_id": "1f06cc6e-7232-6cb1-8000-f71609e6cec5", "checkpoint_ns": ""}}, {'topic':'samosa'})
# now from here with checkpoint id we can execute the state from it





print("\nFINAL STATE:")
print(result)

print("\nJOKE:")
print(result["joke"])


print("\nexplanation:")
print(result["explanation"])