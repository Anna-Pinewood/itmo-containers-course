import streamlit as st
import random
import psycopg2
import os
from datetime import datetime

# Database connection parameters from environment variables
DB_HOST = os.getenv('DB_HOST', 'postgres-service')
DB_NAME = os.getenv('DB_NAME', 'notejardb')
DB_USER = os.getenv('DB_USER', 'notejaruser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'notejarpass')

def init_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    
    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def add_note(note_content):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (content) VALUES (%s)", (note_content,))
    conn.commit()
    cur.close()
    conn.close()

def get_random_note():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT content FROM notes ORDER BY RANDOM() LIMIT 1")
    note = cur.fetchone()
    cur.close()
    conn.close()
    return note[0] if note else None

# Initialize database connection
try:
    init_db()
except Exception as e:
    st.error(f"Database connection error: {e}")

st.title("Note Jar 🫙")

# Input form
with st.form("note_form"):
    note = st.text_area("Write your note:")
    submitted = st.form_submit_button("Drop to the jar")
    
    if submitted and note:
        try:
            add_note(note)
            st.success("Note dropped in the jar! 🫙")
        except Exception as e:
            st.error(f"Error saving note: {e}")

# Random note picker
if st.button("Pick random note from jar"):
    try:
        random_note = get_random_note()
        if random_note:
            st.info(f"Here's your note: {random_note}")
        else:
            st.warning("The jar is empty! Add some notes first.")
    except Exception as e:
        st.error(f"Error retrieving note: {e}")