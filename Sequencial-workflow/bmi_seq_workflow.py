from langgraph.graph import StateGraph , START , END
from typing import TypedDict


#Define state 

class BMIState():

    weight_kg: float
    height_m: float
    bmi: float
    category: str



#define graph

graph = StateGraph(BMIState)

#add nodes to the graph

def calculate_bmi(state: BMIState) -> BMIState:
    weight = state['weight_kg']
    height = state['height_m']

    bmi = weight/(height**2)

    state['bmi']=round(bmi,2)

    return state


def label_bmi(state: BMIState) -> BMIState:

    bmi = state['bmi']

    if bmi < 18.5:
        state['category']='underweight'
    elif 18.5 <= bmi < 25:
        state['category']='normal'
    elif 25 <= bmi < 30:
        state['category'] = 'overweight'
    else:
        state['category'] = 'obese'

    return state



graph.add_node('calculate_bmi', calculate_bmi)
graph.add_node('label_bmi',label_bmi)


#add edges to the graph


graph.add_edge(START,'calculate_bmi')
graph.add_edge('calculate_bmi','label_bmi')
graph.add_edge('label_bmi',END)


#compile the graph

workflow = graph.compile()

# print(workflow)

#execute the graph

outputstate = workflow.invoke({'weight_kg':50 , 'height_m':1.74})
print(outputstate)


# print(graph)