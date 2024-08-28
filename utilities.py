import requests
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import sqlite3
import requests
import json
from langchain_community.utilities.sql_database import SQLDatabase
import os
from groq import Groq
from dotenv import load_dotenv
from settings import env
# loading variables from .env file
load_dotenv() 

dash_line = '-'.join('' for x in range(100))

NL_TO_SQL_API = env.ngrok["ngrok_api"]

def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

def database_from_sqlitefile(sql_file):
    """Read SQL file from local path, populate in-memory database, and create engine."""
    with open(sql_file, 'r') as file:   
        sql_script = file.read()

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

def get_nlp_to_sql_results(question, schema):

    url = f"{NL_TO_SQL_API}/generate-sql"

    payload = json.dumps({
    "question": question,
    "schema" : schema
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print("response : ", response.json())
    return response.json()['sql_query']

def query_to_answer(query, db):
    from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
    execute_query = QuerySQLDataBaseTool(db=db)
    answer = execute_query.invoke(query)
    print("answer: ",answer)
    return answer

def generate_rephrased_answer(question, answer):
    api_key = env.groq["groq_api"]
    model_name = "llama-3.1-8b-instant"

    client = Groq(api_key=api_key)
    
    messages = [
        {
            "role": "system",
            "content": (
            """ You are a good assistant for rephrasing answers. I will give you the question 
                and answer, and you have to rewrite the answer with one like this:\n
                For example:\
                Question: How many orders are there?\n
                Answer: [(412,)]\n
                Response: There are a total of 412 orders.\n\n

                Question: give me a top five customers who spend more
                Answer: [('Helena', 'Holý', 49.620000000000005), ('Richard', 'Cunningham', 47.620000000000005), ('Luis', 'Rojas', 46.62), ('Ladislav', 'Kovács', 45.62), ('Hugh', "O'Reilly", 45.62)]
                Response:
                    The top four customers based on their spending are:
                    1. Helena Holý with a total of $49.62,
                    2. Richard Cunningham with a total of $47.62,
                    3. Luis Rojas with a total of $46.62,
                    4. (tied) Ladislav Kovács and Hugh O'Reilly both with a total of $45.62.

                If you are not able to generate the response, then return the response as 
                \"I am not able to find the answer.\""""
            )
        },
        {
            "role": "user",
            "content": f"question = {question}\nanswer = {answer}"
        }
    ]
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=1,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    print('generate_rephrased_answer' ,response)
    print(dash_line)
    return response