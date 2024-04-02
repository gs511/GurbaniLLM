import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="👋",
    layout="wide"

)

st.write("# Welcome to Gurbani Search LLM! 👋")

st.sidebar.success("Click Gurbani Search to get started 👆")

st.markdown(
    """
    This is a simple Gurbani Contextual search app. Enter your query about any topic in the text box,
      and the app will find the most similar shabads from the database . The Database consist of shabds 
      from various sources such as Sri Guru Granth Sahib, Dasam Granth and others.. Currently, only about
        300 angs of Guru granth sahib are stored in Pinecone Vector DB and open AI model is used to generate
          embeddings.

    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!

    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
"""
)

st.header("Watch Quick Start Guide")

st.video(data="https://www.youtube.com/watch?v=HAZwj23DxVE")