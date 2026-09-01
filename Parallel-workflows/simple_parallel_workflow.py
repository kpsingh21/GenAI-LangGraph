from langgraph.graph import StateGraph ,START,END
from typing import TypedDict

class BatsmanState(TypedDict):
    
    runs: int
    balls: int
    fours: int
    sixes: int

    sr: float  #strikerate
    bpb: float #boundariesperball
    boundary_percent: float 


graph = StateGraph(BatsmanState)

def calculate_sr(state: BatsmanState):
    sr = (state['runs']/state['balls'])*100
    state['sr']=sr
    # return state  this syntax give error
    return {'sr': sr}

def calculate_bpb(state: BatsmanState):
    bpb = state['balls']/(state['fours']+state['sixes'])
    state['bpb']=bpb
    return {'bpb': bpb}

def calculate_boundary_percent(state: BatsmanState):

    boundary_percent = (((state['fours'] * 4) + (state['sixes'] * 6))/state['runs'])*10
    state['boundary_percent'] = boundary_percent
    return {'boundary_percent': boundary_percent}

def summary(state: BatsmanState):

    summary = f"""
    Strike Rate - {state['sr']} \n
    Balls per boundary - {state['bpb']} \n
    Boundary percent - {state['boundary_percent']}
    """
    return {'summary': summary}


# langgraph.errors.InvalidUpdateError: At key 'runs': Can receive only one value per step. Use an Annotated key to handle multiple values.
# For troubleshooting, visit: https://docs.langchain.com/oss/python/langgraph/errors/INVALID_CONCURRENT_GRAPH_UPDATE

# Actually  here we are returning the whole state at every fun  & this fun are executing in parallel so it consoder that every step or fun all the value is changing so returning state is not the correct way


#add node
graph.add_node('calculate_sr', calculate_sr)
graph.add_node('calculate_bpb', calculate_bpb)
graph.add_node('calculate_boundary_percent', calculate_boundary_percent)
graph.add_node('summary', summary)


#add edges

graph.add_edge(START, 'calculate_sr')
graph.add_edge(START, 'calculate_bpb')
graph.add_edge(START, 'calculate_boundary_percent')

graph.add_edge('calculate_sr', 'summary')
graph.add_edge('calculate_bpb', 'summary')
graph.add_edge('calculate_boundary_percent', 'summary')

graph.add_edge('summary', END)

workflow = graph.compile()


inital_state = { 
    'runs': 100,
    'balls': 50,
    'fours': 6,
    'sixes': 4
}

res = workflow.invoke(inital_state)
print(res)
