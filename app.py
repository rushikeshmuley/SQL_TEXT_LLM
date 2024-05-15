# load all the enviroment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure our api Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Model and Provide sql query as Response

def get_gemini_reponse(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Function to retrieve query from database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

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
        rows = read_sql_query(response, "student.db")
        if rows:
            st.subheader("Result:")
            for row in rows:
                st.write(row)
        else:
            st.warning("No results found.")
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")

