import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from utilities import get_engine_for_chinook_db, get_nlp_to_sql_results, query_to_answer, generate_rephrased_answer

st.title("Langchain NL2SQL Chatbot")

# File uploader in the sidebar
with st.sidebar:
    st.write("")  # Adjust the number of placeholders as needed
    uploaded_file = st.file_uploader("Upload a file", type=None)


# Initialize chat history
if "messages" not in st.session_state:
    # print("Creating session state")
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


engine = get_engine_for_chinook_db()
db = SQLDatabase(engine)
schema = db.table_info


# Accept user input
if prompt := st.chat_input("What is up?"):

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    
    response = get_nlp_to_sql_results(question= prompt, schema=schema)
    executed_answer =  query_to_answer(query=response, db=db)
    rephrased_answer = generate_rephrased_answer(question=prompt, answer=executed_answer)

    # Display assistant response in chat message container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            st.markdown(rephrased_answer)
    st.session_state.messages.append({"role": "assistant", "content": rephrased_answer})