#promt chaining workflow means when we are using llm more then one time


from langgraph.graph import StateGraph , START,END
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

class BlogState(TypedDict):
    topic: str
    outline: str
    content: str


graph = StateGraph(BlogState)

def generate_outline(state: BlogState):
    #fetch topic
    topic = state['topic']
    #call llm genrate 
    prompt = f'genrate a outline for a blog on thr topic - {topic}'
    otline=model.invoke(prompt).content
    #update state
    state['outline']=otline

    return state



def generate_blog(state: BlogState):

    topic = state['topic']
    outline = state['outline']
    prompt = f'write a detail blog on the {outline}'
    blog = model.invoke(prompt).content

    state['content']=blog

    return state




#add node
graph.add_node('generate_outline',generate_outline)
graph.add_node('generate_blog',generate_blog)


#add edges

graph.add_edge(START,'generate_outline' )
graph.add_edge('generate_outline','generate_blog' )
graph.add_edge('generate_blog',END )


#compile

workflow =graph.compile()

#invoke
initial_state = { 'title': 'Rise of AI in india'}

final_state = workflow.invoke(initial_state)

print(final_state['outline'])
print(final_state['content'])


# in langchain we will get the final output direct here we are able to see the intermediate result also this is the one of the reason ir benfit of langraph









