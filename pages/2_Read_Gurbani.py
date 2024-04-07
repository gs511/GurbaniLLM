import streamlit as st
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import numpy as np
load_dotenv()
import banidb

# st.set_page_config(layout="wide")
st.set_page_config(page_title="Read Gurbani", page_icon="📈",layout="wide")


# pc = Pinecone(api_key=os.getenv('PINECONE_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

# Streamlit UI
col1, col2 = st.columns(2)

if "selected_source" not in st.session_state:
    st.session_state["selected_source"] = None

if "shabad_dict" not in st.session_state:
    st.session_state["shabad_dict"] = None

if "current_shabad_id" not in st.session_state:
    st.session_state["current_shabad_id"] = None

source = st.sidebar.radio(
    "Select Gurbani to Read",
    ("SGGS", "Dasam Granth", 'Bhai Gurdas Ji','Bhai Nand Lal Ji'),
    # on_change=get_shabad
)
st.session_state["selected_source"] = source

display_type = st.sidebar.radio(
    "Choose Display type",
    ("Punjabi and English","Punjabi Only")
)

def get_shabad():
    shabad_dict = get_bani_shabad(st.session_state["selected_source"])
    st.session_state['shabad_dict'] = shabad_dict

with st.sidebar:
    st.button("Select Bani", on_click=get_shabad)

def get_full_shabad(shabad_id):
    # return shabad in eng and punjabi
    try:
        shabad_dict = banidb.shabad(shabad_id)
    except KeyError as ke:
        print("shabad_id does not exist")
        return None
    
    shabad_text_pa = ""
    shabad_text_eng = ""
    for verse in shabad_dict['verses']:
        shabad_text_pa += verse['verse'] 
        if verse["steek"]["en"]["bdb"] is not None:
            shabad_text_eng += verse["steek"]["en"]["bdb"]  #multiple english steeks available, choosing bdb
        else:
            shabad_text_eng += " "
    return {"shabad_text_pa":shabad_text_pa,
            "shabad_text_eng":shabad_text_eng,
            "shabad_id":shabad_dict["shabad_id"]}


def get_bani_shabad(source):
    # pagination included by default, multiple calls to this function increment shabad index.
    # is this the best approch? not sure. Not a good ide. Decoupling it
    if source == "SGGS":
        if not st.session_state["current_shabad_id"]:
            st.session_state['current_shabad_id'] = 1
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad
        else:
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad

    if source == "Bhai Gurdas Ji":
        if not st.session_state["current_shabad_id"]:
            st.session_state['current_shabad_id'] = 41000
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad
        else:
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad

    if source == "Bhai Nand Lal Ji":
        if not st.session_state["current_shabad_id"]:
            st.session_state['current_shabad_id'] = 32001
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad
        else:
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad  

    if source == "Dasam Granth":
        if not st.session_state["current_shabad_id"]:
            st.session_state['current_shabad_id'] = 7402
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad
        else:
            full_shabad = get_full_shabad(st.session_state['current_shabad_id'])
            return full_shabad    

def chat_widget_helper(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages.chat_message("user").write(prompt)
    # with messages.chat_message("assistant"):
    response_generator = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        temperature=0, stream=True)
    response = messages.chat_message("assistant").write_stream(response_generator)
    st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    # st.title("Chat with Shabads")
    # st.markdown("Ask any question such as - the origin of the word or explain Gurbani to a 5 year old.")
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = [{'role':'system', 'content':"You are a helpful assistant that assit people in understanding Gurbani in a better way by using your knowledge of languages such as punjabi, urdu, persian, farsi, arabic and many more. Since we are dealing with multiple languages, make sure to use only valid Unicode output. Do not make up unicode output if you are not sure. "},
                                     {'role': 'assistant', 'content':"How can I help you with understanding Gurbani today?"}]
    
    messages = st.container(height=650)

    for message in st.session_state.messages:
        if message["role"] == 'system':
            continue
        messages.chat_message(message["role"]).write(message["content"])
        # with messages.chat_message(message["role"]):
        #     messages.write(message["content"])

    if prompt := st.chat_input("Say something"):
        chat_widget_helper(prompt)
    # print(st.session_state.messages)
    #     # messages.chat_message("assistant").write(f"Echo: {prompt}")


with col1:
        st.title("Read Gurbani")
        if st.session_state['selected_source'] == "Bhai Gurdas Ji":
            shabad_index = st.slider('choose shabad',min_value=0,max_value=711,value=None,step=1)
            shabad_index += 41000
        if st.session_state['selected_source'] == "Bhai Nand Lal Ji":
            shabad_index = st.slider('choose shabad',min_value=0,max_value=1000,value=None,step=1)
            shabad_index += 32001
        if st.session_state['selected_source'] == "Dasam Granth":
            shabad_index = st.slider('choose shabad',min_value=0,max_value=5398,value=None,step=1)
            shabad_index += 7402
        if st.session_state['selected_source'] == "SGGS":
            shabad_index = st.slider('choose shabad',min_value=1,max_value=7401,value=None,step=1)
            print(shabad_index,'shabad_index')
        if shabad_index != 0:
            if st.session_state['current_shabad_id']:
                st.session_state['current_shabad_id'] = shabad_index
                st.session_state['shabad_dict'] = get_bani_shabad(st.session_state['selected_source'])
            else:
                st.warning('Please select a Bani First.')
        # print('source,,,', source)
        button2 = st.button("next",key="3343")
        if button2:
            # print('next button pressed')
            if st.session_state['current_shabad_id']:
                # print(st.session_state['current_shabad_id'])
                st.session_state['current_shabad_id'] = st.session_state['current_shabad_id'] + 1
                # print(st.session_state['current_shabad_id'])
                st.session_state['shabad_dict'] = get_bani_shabad(st.session_state['selected_source'])
            else:
                st.warning('Please select a Bani First.')
        
        with st.container(height=500):
            shabad = st.session_state['shabad_dict']
            if shabad:
                # print(shabad,'LllLL')
                # for element in st.session_state.simDocs:
                with st.form(key=str(shabad['shabad_id']), border=False):
                    if display_type == "Punjabi Only":
                        txt = shabad['shabad_text_pa']
                        st.write(txt)
                    else:
                        txt = shabad['shabad_text_pa'] + "   @   " + shabad['shabad_text_eng']
                        st.write(txt)
                    # Every form must have a submit button.
                    c1, c2, c3 = st.columns([1, 1, 1], gap="small")
                    # with c1:
                    #     submitted1 = st.form_submit_button("Explain more")
                    #     if submitted1:
                    #         # st.write('button cliked')
                    #         chat_widget_helper("Explain the following Gurbani using your knowldege: " + txt)
                    with c1:
                        submitted2 = st.form_submit_button("Explain Root Words")
                        if submitted2:
                            chat_widget_helper("Explain the uncommon punjabi words by breaking down into their root words and its meanings and origin: " + txt)
                    with c3:
                        submitted3 = st.form_submit_button("Explain to 5 yr old")
                        if submitted3:
                            chat_widget_helper("Explain the following shabad to a 5 year old in easy language: " + txt)

# print(st.session_state)