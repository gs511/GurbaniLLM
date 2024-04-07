import streamlit as st
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import numpy as np
load_dotenv()
# st.set_page_config(layout="wide")
st.set_page_config(page_title="Gurbani Search", page_icon="📈",layout="wide")


pc = Pinecone(api_key=os.getenv('PINECONE_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

def get_embedding(text, model="text-embedding-3-small"):
  #  text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def search_shabads(query):
# create the query vector
    if query:
        xq = get_embedding(query)
    else:
        xq = list(np.random.random(1536))
    # now query
    index = pc.Index("bani-db-serverless")
    if source == 'All':
        xc = index.query(vector=xq, top_k=num_docs, include_metadata=True,namespace="pankti_combined")
    else:
        xc = index.query(vector=xq, top_k=num_docs, include_metadata=True,namespace="pankti_combined",filter={"source":source})
    return [match["metadata"] for match in xc['matches']]

# Streamlit UI
col1, col2 = st.columns(2)
                   
num_docs = st.sidebar.slider('How many similar docs to return?', 1, 50, 5)
source = st.sidebar.radio(
    "Choose a Gurbani source",
    ("All","SGGS", "Dasam Granth", 'Bhai Gurdas Ji','Bhai Nand Lal Ji')
)
display_type = st.sidebar.radio(
    "Choose Display type",
    ("Punjabi and English","Punjabi Only")
)

# st.sidebar.info(
#     "This is a simple Gurbani Contextual search app. "
#     "Enter your query about any topic in the text box, and the app will find the most similar shabads from the database\
#         . The Database consist of shabds from various sources such as Sri Guru Granth Sahib, Dasam Granth and others..\
#             Currently, only about 300 angs of Guru granth sahib are stored in Pinecone Vector DB and open AI model is\
#                 used to generate embeddings."
# )


def onExplainButtonClick(text):
    pass


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
    st.title("Chat with Shabads")
    st.markdown("Ask any question such as - the origin of the word or explain Gurbani to a 5 year old.")
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


def similar_search_helper(user_query=None):
    st.session_state.simDocs = [] 
    #new query has been run, save updated results to store state. Rewrite over any exisiting data
    # start a new search
    # Find similar documents
    similar_documents = search_shabads(user_query)
    for id_,doc in enumerate(similar_documents):
        if display_type == "Punjabi Only":
            st.session_state.simDocs.append({'doc':doc['shabad_pa'],'id_':id_})
        else:
            st.session_state.simDocs.append({ 'doc': doc['shabad_pa'] + "   @   " + doc['shabad_eng'],
                                            'id_': id_})

with col1:

#    st.write("This is inside the container")
    st.title("Contextual Search")
    # Input box for user query
    if "simDocs" not in st.session_state:
        st.session_state.simDocs = [] #storing docs to maintain state
    with st.form('main-form',border=False):
        st.markdown("Enter topic in English or Punjabi. Examples: stages of life, metaphors for love, 5 vices, importance of Guru ..etc",
                    help='Bamboo, chandan, importance of human life, Grihast, Household life vs Ascetic life')
        user_query = st.text_input("",placeholder="stages of life",label_visibility='collapsed')
        c1, c2 = st.columns([1, 1], gap="small")
        with c1:
            submitted1 = st.form_submit_button("Search")
            if submitted1:
                if user_query:
                    similar_search_helper(user_query)
                    
                else:
                    st.warning("Please enter a query.")

        with c2: #random query
            submitted2 = st.form_submit_button("Random Search")
            if submitted2:
                similar_search_helper()

    st.markdown("Search Results:")
    with st.container(height=550):
        for element in st.session_state.simDocs:
            with st.form(key=str(element['id_']), border=True):
                st.write(element['doc'])
                # Every form must have a submit button.
                c1, c2, c3 = st.columns([1, 1, 1], gap="small")
                with c1:
                    submitted1 = st.form_submit_button("Explain more")
                    if submitted1:
                        # st.write('button cliked')
                        chat_widget_helper("Explain the following Gurbani using your knowldege: " + element['doc'])
                with c2:
                    submitted2 = st.form_submit_button("Explain Root Words")
                    if submitted2:
                        chat_widget_helper("Explain the punjabi words by breaking down into their root words and its meanings and origin: " + element['doc'])
                with c3:
                    submitted3 = st.form_submit_button("Explain to 5 yr old")
                    if submitted3:
                        chat_widget_helper("Explain the following shabad to a 5 year old in easy language: " + element['doc'])

            # st.write(element['doc'])
            # st.button('explain',key=element['id_'])

# ਹਉ ਵਾਰੀ ਜੀਉ ਵਾਰੀ ਨਿਰੰਕਾਰੀ ਨਾਮੁ ਧਿਆਵਣਿਆ ॥ਤਿਸੁ ਰੂਪੁ ਨ ਰੇਖਿਆ ਘਟਿ ਘਟਿ ਦੇਖਿਆ ਗੁਰਮੁਖਿ ਅਲਖੁ ਲਖਾਵਣਿਆ @ I am a sacrifice, my soul is a sacrifice, to those who meditate on the Naam, the Name of the Formless Lord.He has no form or shape; He is seen within each and every heart. The Gurmukh comes to know the unknowable.
#  openAI unicode error-rare error use for debug