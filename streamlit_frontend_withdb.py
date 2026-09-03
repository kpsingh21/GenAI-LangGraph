import streamlit as st
from chatbot_with_db import chatbot , retrive_all_threads
from langchain_core.messages import BaseMessage , HumanMessage

import uuid

# utility fun

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
       st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])

# session setup
if 'message_history' not in  st.session_state:
    st.session_state['message_history']=[]


if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()


if 'chat_threads' not in st.session_state:
    # st.session_state['chat_threads']=[]
    st.session_state['chat_threads']=retrive_all_threads()


add_thread(st.session_state['thread_id'])

# sidebar ui

st.sidebar.title('Langgraph Chatbot')


if st.sidebar.button('New chat'):
      reset_chat()


st.sidebar.header('My conversations')




# this display only current thread id we need to show all thread ids
# st.sidebar.text(st.session_state['thread_id'])

# for thread_id in st.session_state['chat_threads']:
#     st.sidebar.text(thread_id)


for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages

#

# load previous msg 
for msg in  st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])


user_input = st.chat_input('Ask anything')

if user_input:
    #first add the msg to message_history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    # this is code with streaming

    config = { 'configurable': {'thread_id': st.session_state['thread_id'] }}

    with st.chat_message('assistant'):
       ai_msg= st.write_stream(
         message_chunk.content for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=config,
            stream_mode='messages')
        )
    
    st.session_state['message_history'].append({'role':'assistant','content':ai_msg})




