import streamlit as st
import numpy as np
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
import os
load_dotenv()


pc = Pinecone(api_key=os.getenv('PINECONE_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

def get_embedding(text, model="text-embedding-3-small"):
  #  text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def search_shabads(query):
# create the query vector
    xq = get_embedding(query)
    # now query
    index = pc.Index("bani-db-serverless")
    xc = index.query(vector=xq, top_k=5, include_metadata=True,namespace="punjabi-and-english-separate-then-combined")
    return [match["metadata"]["shabad_pa"] for match in xc['matches']]

# Streamlit UI
st.sidebar.title("About")
st.sidebar.info(
    "This is a simple Gurbani Contextual search app. "
    "Enter your query about any topic in the text box, and the app will find the most similar shabads from the database\
        . The Database consist of shabds from various sources such as Sri Guru Granth Sahib, Dasam Granth and others..\
            Currently, only about 300 angs of Guru granth sahib are stored in Pinecone Vector DB and open AI model is\
                 used to generate embeddings."
)

st.title("Gurbani Contextual Search")

# Input box for user query
user_query = st.text_input("Enter your query either in English or Punjabi:")

# Search button
if st.button("Search"):
    if user_query:
        # Find similar documents
        similar_documents = search_shabads(user_query)
        st.header("Most Similar Shabads:")
        for doc in similar_documents:
            st.write(doc)
    else:
        st.warning("Please enter a query.")

