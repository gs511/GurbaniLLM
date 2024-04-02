import streamlit as st

st.set_page_config(
    page_title="Gurbani Search",
    page_icon="📖",
    layout="wide"

)

st.write("# Welcome to Gurbani Search LLM! 👋")

st.sidebar.success("Click Gurbani Search to get started 👆")

st.markdown(
    """
Welcome to Gurbani Search LLM! 👋 Explore Gurbani with our intuitive contextual search app. 

📚 Enter your query on any topic, such as "5 vices", or "stages of life" and the app fetches the most relevant shabads from our extensive database,
 sourced from Sri Guru Granth Sahib, Dasam Granth, and more. 

🙏 Currently housing approximately 2000 shabads in our Pinecone Vector DB, we harness the power of open AI models to generate embeddings, 
 enriching the contextual search. 

🌟 While our app aids in deciphering complex words rooted in Farsi or Sanskrit, please exercise caution and consult traditional sources for in-depth Gurbani explanations. 
Let's create a better Gurbani reading experience together! 🌿

👈 Select Gurbani Search from the sidebar or watch quick start guide below to get started.
🧐 We value your input! Don't hesitate to share your feedback by connecting on [LinkedIn](https://www.linkedin.com/in/gurmukh-singh-a36538118/)
"""
)

st.header("Watch Quick Start Guide")

st.video(data="https://youtu.be/eno7AsjjnWc")