# load all the enviroment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
# import sqlite3

import mysql.connector
import google.generativeai as genai

## Configure our api Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Model and Provide sql query as Response

def get_gemini_reponse(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

# Function to retrieve query from database

# def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
#   db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
#   return SQLDatabase.from_uri(db_uri)

def read_sql_query(sql, db):
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="3306",
        user="root",
        password="12345",
        database="youtube.db"
    )
    
    # Create cursor
    cur = conn.cursor()

    # Execute SQL query
    cur.execute(sql)

    # Fetch all rows
    rows = cur.fetchall()

    # Close cursor and connection
    cur.close()
    conn.close()

    return rows



# def read_sql_query(sql,db):
#     conn=sqlite3.connect(db)
#     cur=conn.cursor()
#     cur.execute(sql)
#     rows=cur.fetchall()
#     conn.commit()
#     conn.close()
#     return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL queries!
    Consider you have a SQL database with the name STUDENT and it contains the following columns - NAME, CLASS, SECTION.
    \n\nFor instance,
    Example 1 - How many entries are there in the database?
    SQL command: SELECT COUNT(*) FROM STUDENT;
    \nExample 2 - Retrieve all the students enrolled in a specific class, say Chemistry.
    SQL command: SELECT * FROM STUDENT WHERE CLASS="Chemistry";
    Ensure that the SQL code doesn't include ``` in the beginning or end, and avoid mentioning "sql" in the output.
    """
]


## streamlit App

st.set_page_config(page_title="Text to SQL LLM", page_icon=":bar_chart:")
st.title(":gem: Gemini App to Retrieve SQL Data")

question=st.text_input("Input:",key="input")

submit=st.button('Ask the question')

# if submit is clicked

if submit:
    response=get_gemini_reponse(question,prompt)
    st.subheader("Generated SQL Query:")
    st.code(response)

    # Execute SQL Query
    try:
        rows = read_sql_query(response, "youtube.db")
        if rows:
            st.subheader("Result:")
            for row in rows:
                st.write(row)
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")


# Display image with code

image = "D:\SQL_TEXT_LLM\SQL.png"  # Replace with your image URL
st.image(image, caption='Generated SQL Code', use_column_width=True)








