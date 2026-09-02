import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import BaseMessage , HumanMessage


# every time this message_history is becaming empty as  streamlit run  line by line on user input so will use 
# message_history = []
# st.session_state --->this is also a dict

if 'message_history' not in  st.session_state:
    st.session_state['message_history']=[]


# loading the conversion history
# for msg in message_history:
#     with st.chat_message(msg['role']):
#         st.text(msg['content'])

for msg in  st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

# with st.chat_message('user'):
#     st.text('Hi')


# with st.chat_message('assistant'):
#     st.text('hi how can i help')


# in streamlit the scipt will start from start so we are not able to store conversional history


user_input = st.chat_input('Ask anything')

if user_input:
    #first add the msg to message_history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    

    # this is dummy now here we need AI input
    config = { 'configurable': {'thread_id': 1}}
    res = chatbot.invoke({'messages': [HumanMessage(content=user_input)]},config=config)
    ai_res = res['messages'][-1].content
    # message_history.append({'role':'assistant','content':user_input})
    st.session_state['message_history'].append({'role':'assistant','content':ai_res})
    with st.chat_message('assistant'):
        st.text(ai_res)






