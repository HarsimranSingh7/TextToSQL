import sqlite3
import pandas as pd
import streamlit as st  # Add this import

def execute_sql_query(sql_query, db_path="student.db"):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        return pd.DataFrame()

def get_table_schema(db_path="student.db"):
    schema = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            table = table_name[0]
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            schema[table] = columns
        conn.close()
    except Exception as e:
        st.error(f"Error retrieving table schema: {e}")
    return schema
