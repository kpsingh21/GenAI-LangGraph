# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
# from pydantic import BaseModel, Field
# from typing import Literal
# from dotenv import load_dotenv
# import json

# load_dotenv()

# llm = HuggingFaceEndpoint(
#     repo_id="Qwen/Qwen3.8-2.4T-A95B",
#     task="conversational",  # Changed from text-generation
#     timeout=300,
#     max_new_tokens=100,
#     temperature=0, #want deterministic classification rather than creative generation.
# )

# model = ChatHuggingFace(llm=llm)


# class SentimentSchema(BaseModel):
#     sentiment: Literal["positive", "negative"] = Field(
#         description="Sentiment of the review"
#     )


# prompt = """
# Analyze the sentiment of the following review.

# Review:
# "The software is too bad"

# Return ONLY valid JSON in exactly this format:

# {"sentiment": "positive"}

# The value must be either "positive" or "negative".
# """

# response = model.invoke(prompt)

# print("Raw response:", response.content)

# data = json.loads(response.content)

# result = SentimentSchema(**data)

# print(result)
# print(result.sentiment)




# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain_core.prompts import PromptTemplate
# from pydantic import BaseModel, Field
# from typing import TypedDict, Literal
# from dotenv import load_dotenv
# from langgraph.graph import StateGraph, START, END
# from langchain_openai import ChatOpenAI
# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

# load_dotenv()


# class SentimentSchema(BaseModel):
#     sentiment: Literal["positive", "negative"] = Field(
#         description="Sentiment of the review"
#     )



# class DiagnosisSchema(BaseModel):
#     issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(description='The category of issue mentioned in the review')
#     tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description='The emotional tone expressed by the user')
#     urgency: Literal["low", "medium", "high"] = Field(description='How urgent or critical the issue appears to be')



# llm = HuggingFaceEndpoint(
#     repo_id="Qwen/Qwen3.8-2.4T-A95B",
#     task="conversational",  # Changed from text-generation
#     max_new_tokens=100,
#     temperature=0,
# )

# model = ChatHuggingFace(llm=llm)

# parser = PydanticOutputParser(
#     pydantic_object=SentimentSchema
# )

# parser2 = PydanticOutputParser(
#     pydantic_object=DiagnosisSchema
# )

# # prompt = PromptTemplate(
# #     template="""
# # Analyze the sentiment of the following review.

# # Review:
# # {review}

# # {format_instructions}
# # """,
# #     input_variables=["review"],
# #     partial_variables={
# #         "format_instructions": parser.get_format_instructions()
# #     },
# # )

# # structured_model = prompt | model | parser
# # structured_model2 = prompt2 | model | parser2



# class ReviewState(TypedDict):
#     review: str
#     sentiment: Literal["positive","negative"]
#     diagnosis: dict
#     response: str


# graph = StateGraph(ReviewState)


# def find_sentiment(state:ReviewState):
#     prompt = f'For the following review find out the statement \n {state['review']}'
#     structured_model = prompt | model | parser
#     sentiment = structured_model.invoke(prompt).sentiment
#     return {'sentiment':sentiment}

    
# def check_sentiment(state: ReviewState) -> Literal["positive_response","run_diagnosis"]:

#     if state['sentiment'] == 'positive':
#         return 'positive_response'
#     else:
#         return 'run_diagnosis'


# def positive_response(state: ReviewState):

#     prompt = f"""Write a warm thank-you message in response to this review:
#     \n\n\"{state['review']}\"\n
# Also, kindly ask the user to leave feedback on our website."""

#     structured_model = prompt | model | parser

    
#     response = structured_model.invoke(prompt).content

#     return {'response': response}

# def run_diagnosis(state: ReviewState):

#     prompt = f"""Diagnose this negative review:\n\n{state['review']}\n"
#     "Return issue_type, tone, and urgency.
# """

#     structured_model2 = prompt2 | model | parser2

#     response = structured_model2.invoke(prompt)

#     return {'diagnosis': response.model_dump()}

# def negative_response(state: ReviewState):

#     diagnosis = state['diagnosis']

#     prompt2 = f"""You are a support assistant.
# The user had a '{diagnosis['issue_type']}' issue, sounded '{diagnosis['tone']}', and marked urgency as '{diagnosis['urgency']}'.
# Write an empathetic, helpful resolution message.
# """

#     structured_model2 = prompt2 | model | parser2

#     response = structured_model2.invoke(prompt2).content

#     return {'response': response}


# graph.add_node('find_sentiment',find_sentiment)
# graph.add_node('run_diagnosis', run_diagnosis)
# graph.add_node('positive_response', positive_response)
# graph.add_node('negative_response', negative_response)



# graph.add_edge(START,'find_sentiment')
# graph.add_conditional_edges('find_sentiment', check_sentiment)

# graph.add_edge('positive_response', END)

# graph.add_edge('run_diagnosis', 'negative_response')
# graph.add_edge('negative_response', END)


# workflow = graph.compile()

# intial_state = {
#     'review': "I’ve been trying to log in for over an hour now, and the app keeps freezing on the authentication screen. I even tried reinstalling it, but no luck. This kind of bug is unacceptable, especially when it affects basic functionality."
# }

# workflow.invoke(intial_state)



# result = chain.invoke({
#     "review": "The software is too bad"
# })

# print(result)
# print(result.sentiment)




# prompt | model | parser

# where prompt is a string. The | composition should use a LangChain Runnable such as PromptTemplate, not a plain string.

# Also, your positive response and negative response should NOT use the sentiment/diagnosis Pydantic parsers, because those nodes need a normal text response.

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

load_dotenv()


# ============================================================
# 1. PYDANTIC SCHEMAS
# ============================================================

class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the review")


class DiagnosisSchema(BaseModel):
    issue_type: Literal[ "UX", "Performance", "Bug", "Support", "Other"] = Field(description="The category of issue mentioned in the review")

    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description="The emotional tone expressed by the user")

    urgency: Literal["low", "medium", "high"] = Field(description="How urgent or critical the issue appears to be")


# ============================================================
# 2. MODEL
# ============================================================

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.8-2.4T-A95B",
    task="conversational",
    max_new_tokens=200,
    temperature=0,
)

model = ChatHuggingFace(llm=llm)


# ============================================================
# 3. OUTPUT PARSERS
# ============================================================

sentiment_parser = PydanticOutputParser(
    pydantic_object=SentimentSchema
)

diagnosis_parser = PydanticOutputParser(
    pydantic_object=DiagnosisSchema
)


# ============================================================
# 4. PROMPTS
# ============================================================

sentiment_prompt = PromptTemplate(
    template="""
Analyze the sentiment of the following review.

Review:
{review}

{format_instructions}
""",
    input_variables=["review"],
    partial_variables={
        "format_instructions": sentiment_parser.get_format_instructions()
    },
)


diagnosis_prompt = PromptTemplate(
    template="""
Diagnose the following negative review.

Review:
{review}

Determine:
1. issue_type
2. tone
3. urgency

{format_instructions}
""",
    input_variables=["review"],
    partial_variables={
        "format_instructions": diagnosis_parser.get_format_instructions()
    },
)


# ============================================================
# 5. STRUCTURED CHAINS
# ============================================================

sentiment_chain = sentiment_prompt | model | sentiment_parser

diagnosis_chain = diagnosis_prompt | model | diagnosis_parser


# ============================================================
# 6. LANGGRAPH STATE
# ============================================================

class ReviewState(TypedDict, total=False):
    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict
    response: str


# ============================================================
# 7. CREATE GRAPH
# ============================================================

graph = StateGraph(ReviewState)


# ============================================================
# 8. NODE: FIND SENTIMENT
# ============================================================

def find_sentiment(state: ReviewState):

    result = sentiment_chain.invoke({
        "review": state["review"]
    })

    return {
        "sentiment": result.sentiment
    }


# ============================================================
# 9. CONDITIONAL ROUTING
# ============================================================

def check_sentiment(
    state: ReviewState
) -> Literal["positive_response", "run_diagnosis"]:

    if state["sentiment"] == "positive":
        return "positive_response"

    return "run_diagnosis"


# ============================================================
# 10. NODE: POSITIVE RESPONSE
# ============================================================

def positive_response(state: ReviewState):

    prompt = f"""
Write a warm thank-you message in response to this review:

"{state['review']}"

Also, kindly ask the user to leave feedback on our website.
"""

    response = model.invoke(prompt).content

    return {
        "response": response
    }


# ============================================================
# 11. NODE: RUN DIAGNOSIS
# ============================================================

def run_diagnosis(state: ReviewState):

    result = diagnosis_chain.invoke({
        "review": state["review"]
    })

    return {
        "diagnosis": result.model_dump()
    }


# ============================================================
# 12. NODE: NEGATIVE RESPONSE
# ============================================================

def negative_response(state: ReviewState):

    diagnosis = state["diagnosis"]

    prompt = f"""
You are a support assistant.

The user had a '{diagnosis["issue_type"]}' issue,
sounded '{diagnosis["tone"]}',
and the urgency is '{diagnosis["urgency"]}'.

Original review:
"{state["review"]}"

Write an empathetic and helpful resolution message.
Do not return JSON. Return only the response to the user.
"""

    response = model.invoke(prompt).content

    return {
        "response": response
    }


# ============================================================
# 13. ADD NODES
# ============================================================

graph.add_node("find_sentiment", find_sentiment)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("positive_response", positive_response)
graph.add_node("negative_response", negative_response)


# ============================================================
# 14. ADD EDGES
# ============================================================

graph.add_edge(START, "find_sentiment")

graph.add_conditional_edges("find_sentiment",check_sentiment)

graph.add_edge("positive_response",END)

graph.add_edge("run_diagnosis","negative_response")

graph.add_edge("negative_response",END)


# ============================================================
# 15. COMPILE
# ============================================================

workflow = graph.compile()


# ============================================================
# 16. INITIAL STATE
# ============================================================

initial_state = {
    "review": """
I’ve been trying to log in for over an hour now, and the app keeps
freezing on the authentication screen. I even tried reinstalling it,
but no luck. This kind of bug is unacceptable, especially when it
affects basic functionality.
"""
}


# ============================================================
# 17. RUN GRAPH
# ============================================================

result = workflow.invoke(initial_state)

print("\nFINAL STATE:")
print(result)

print("\nSENTIMENT:")
print(result["sentiment"])

print("\nDIAGNOSIS:")
print(result.get("diagnosis"))

print("\nRESPONSE:")
print(result["response"])