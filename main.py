import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from utilities import (
    get_engine_for_chinook_db, 
    get_nlp_to_sql_results, 
    query_to_answer, 
    generate_rephrased_answer, 
    database_from_sqlitefile
)
from streamlit_mic_recorder import speech_to_text
import os
import tempfile

def main():

    # Just Title of the page
    st.set_page_config(
        page_title="ChatWithYourDatabase",
        page_icon="👋",
    )
    st.title("NL2SQL Chatbot")
    st.markdown("Chat With Your Database 📊")
    st.divider()

    # File uploader in the sidebar
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload a .sql file", type=["sql"])

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle file upload 
    if uploaded_file is not None:
        try:
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            st.write(f"Uploaded file: {uploaded_file.name}")

            # Load the database from the temporary file
            engine = database_from_sqlitefile(sql_file=temp_file_path)
            db = SQLDatabase(engine)
            schema = db.table_info

            # Display the schema in the sidebar
            with st.sidebar:
                st.subheader("Database Schema")
                # st.text_area("Schema", schema, height=400 , label_visibility = "hidden")
                st.code(schema , language="sql" , line_numbers=True)

            # Clean up the temporary file
            os.remove(temp_file_path)

        except Exception as e:
            st.error(f"Error loading the database: {e}")
            st.stop()
    else:
        st.info("""Please upload a .sql file,
                \n Note: you have uploaded only .sql files with correct schema and permissions""")
        st.stop()

    # Create two columns at the bottom for text input and audio input
    col1, col2 = st.columns([3, 1])

    with col1:
        prompt = st.chat_input("What is up?")

    with col2:
        # st.write("Or use voice input:")
        text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')
        if text:
            prompt = text

    if prompt:
        try:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and execute SQL query
            response = get_nlp_to_sql_results(question=prompt, schema=schema)
            executed_answer = query_to_answer(query=response, db=db)
            rephrased_answer = generate_rephrased_answer(question=prompt, answer=executed_answer)

            # Display assistant response in chat message container
            with st.spinner("Generating response..."):
                with st.chat_message("assistant"):
                    st.markdown(rephrased_answer)

            st.session_state.messages.append({"role": "assistant", "content": rephrased_answer})

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")