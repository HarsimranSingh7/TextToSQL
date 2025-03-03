from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import hashlib
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
from sql import execute_sql_query, get_table_schema

# Load environment variables from .env file
load_dotenv()  # This will still work locally
api_key = os.getenv("GOOGLE_API_KEY")

# Try to get API key from Streamlit secrets if environment variable is not set
if not api_key and hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]

# Check if we have an API key and configure
if not api_key:
    st.error("Google API Key not found. Please set it in .env file or Streamlit secrets.")
    st.stop()
else:
    genai.configure(api_key=api_key)

# Initialize session state
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False
if "suggestion" not in st.session_state:
    st.session_state["suggestion"] = ""
if "query_history" not in st.session_state:
    st.session_state["query_history"] = []
if "query_results" not in st.session_state:
    st.session_state["query_results"] = None

# Authentication function
def authenticate():
    password = st.text_input("Enter Password", type="password", key="password_input")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    stored_password = hashlib.sha256("your_secure_password".encode()).hexdigest()  # Replace with your password hash
    if hashed_password == stored_password:
        st.session_state["is_authenticated"] = True
    elif password:
        st.error("Incorrect Password. Hint: the password is 'your_secure_password'.")

# Function to generate English prompt suggestions
def generate_prompt_suggestion():
    try:
        # Use the correct model name from your curl command
        model = genai.GenerativeModel("gemini-2.0-flash")  # Updated model name
        prompt = """
        Provide a helpful natural language query suggestion to explore a student database.
        Example prompts include:
        - "Show the top 5 students with the highest math scores"
        - "List students who scored above 80 in writing and completed the test preparation course"
        - "Calculate the average reading score by gender"
        """
        response = model.generate_content(prompt)
        st.session_state["suggestion"] = response.text.strip()
    except Exception as e:
        st.error(f"Error generating suggestion: {str(e)}")
        # Provide a fallback suggestion
        st.session_state["suggestion"] = "Show the top 5 students with the highest math scores"

# Generative Model for Natural Language to SQL
def generate_sql_from_text(question, prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    # Concatenate prompt and question into a single string input
    input_text = prompt + "\nQuestion: " + question
    response = model.generate_content(input_text)
    sql_query = response.text.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # Specific instructions for SQLite compatibility
    # Adjust the SQL query if it contains AVG() or other aggregate functions in WHERE clauses
    if "AVG(" in sql_query and ("WHERE" in sql_query or "BETWEEN" in sql_query):
        # Insert a subquery to calculate the aggregate outside of the WHERE clause
        sql_query = (
            "WITH avg_calculation AS (SELECT AVG(MATH_SCORE) AS avg_math_score FROM STUDENT) "
            "SELECT * FROM STUDENT, avg_calculation WHERE READING_SCORE BETWEEN avg_math_score - 5 AND avg_math_score + 5;"
        )
    
    return sql_query

# Main App Interface
def app_interface():
    st.markdown(
        "<h1 style='text-align: center; color: #3B82F6;'>Enhanced Text-to-SQL Application</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "This application translates natural language questions into SQL queries and visualizes the results."
    )

    # Show available tables and schema
    st.markdown("### 📋 Available Tables and Columns")
    schema = get_table_schema("student.db")
    for table, columns in schema.items():
        st.write(f"**Table: {table}** - Columns: {', '.join(columns)}")

    # Query Input Form
    with st.form(key="query_form"):
        question = st.text_input(
            "Enter your question in natural language:", key="input"
        )
        submit_button = st.form_submit_button("Generate SQL and Run Query")

    # Generate SQL query and execute it if form is submitted
    if submit_button:
        prompt = """
        You are a highly skilled SQL assistant, specialized in translating complex natural language questions into accurate SQL queries. You are working with a SQLite database called `STUDENT` with a single table named `STUDENT`. This table has the following columns:
        - `GENDER`
        - `ETHNICITY`
        - `PARENT_EDUCATION`
        - `LUNCH`
        - `PREP_COURSE`
        - `MATH_SCORE`
        - `READING_SCORE`
        - `WRITING_SCORE`

        Keep the following rules in mind while generating SQL queries:
        1. **Target Table and Column Names**: Only use the `STUDENT` table and its exact column names as provided above. Avoid any other table names or column names.
        2. **Aggregate Functions**: Ensure that aggregate functions (like `AVG`, `SUM`, `COUNT`, `MAX`, and `MIN`) are used appropriately. When using aggregate functions in conditions (e.g., filtering results by average scores), use subqueries to ensure compatibility with SQLite.
        3. **Grouping and Filtering**: For queries that require grouping, use `GROUP BY` and include filters such as `HAVING` when necessary. Always ensure that grouped columns are explicitly stated in the `SELECT` clause if using aggregates.
        4. **Complex Conditions**: Handle conditions that require a range or comparisons (like "scores within 5 points of the average") by using subqueries or `WITH` clauses.
        5. **Avoid Backticks or Formatting Errors**: Do not use backticks or unnecessary formatting characters in the SQL syntax.
        6. **Ordering and Limits**: For queries that require ordering (e.g., top students by score), use `ORDER BY` and `LIMIT` where applicable.

        Here are some examples of more complex questions and their respective SQL translations:
        1. "Find the average math score of male students" → `SELECT AVG(MATH_SCORE) AS avg_math_score FROM STUDENT WHERE GENDER = 'male';`
        2. "List the top 3 students with the highest writing scores, showing their gender and writing score" → `SELECT GENDER, WRITING_SCORE FROM STUDENT ORDER BY WRITING_SCORE DESC LIMIT 3;`
        3. "Calculate the average reading score for students grouped by gender and parental education level" → `SELECT GENDER, PARENT_EDUCATION, AVG(READING_SCORE) AS avg_reading_score FROM STUDENT GROUP BY GENDER, PARENT_EDUCATION;`
        4. "Show students who have a reading score within 5 points of the average math score" → `WITH avg_math AS (SELECT AVG(MATH_SCORE) AS avg_math_score FROM STUDENT) SELECT * FROM STUDENT, avg_math WHERE READING_SCORE BETWEEN avg_math.avg_math_score - 5 AND avg_math.avg_math_score + 5;`
        5. "Count the number of students in each lunch type, ordered by the count in descending order" → `SELECT LUNCH, COUNT(*) AS count_students FROM STUDENT GROUP BY LUNCH ORDER BY count_students DESC;`
        6. "Find the maximum and minimum scores in math for each ethnic group" → `SELECT ETHNICITY, MAX(MATH_SCORE) AS max_math, MIN(MATH_SCORE) AS min_math FROM STUDENT GROUP BY ETHNICITY;`

        Based on these guidelines, please generate a valid SQL query for the following question:
        """
        
        sql_query = generate_sql_from_text(question, prompt)
        st.session_state["sql_query"] = sql_query
        st.markdown(
            f"<div style='color: #4B5563;'>Generated SQL Query:</div> `{sql_query}`",
            unsafe_allow_html=True,
        )

        # Execute the SQL query and store results
        try:
            results_df = execute_sql_query(sql_query)
            st.session_state["query_results"] = results_df
        except Exception as e:
            st.error(f"Error executing SQL query: {e}")
            return

        # Add query to history
        st.session_state["query_history"].append((question, sql_query))

    # Display query results
    results_df = st.session_state.get("query_results")
    if results_df is not None and not results_df.empty:
        st.markdown("### 🔍 Query Results")
        st.dataframe(
            results_df.style.set_properties(
                **{"color": "white", "background-color": "#1F2937"}
            )
        )

        # Visualization options
        chart_type = st.selectbox(
            "Choose a Chart Type", ["None", "Bar Chart", "Line Chart", "Pie Chart", "Heatmap", "Scatter Plot"]
        )

        # Display charts based on user selection
        if chart_type == "Bar Chart":
            st.bar_chart(results_df)
        elif chart_type == "Line Chart":
            st.line_chart(results_df.set_index(results_df.columns[0]))
        elif chart_type == "Pie Chart":
            fig, ax = plt.subplots()
            results_df.groupby(results_df.columns[1])[results_df.columns[-1]].sum().plot.pie(ax=ax, autopct="%1.1f%%")
            st.pyplot(fig)
        elif chart_type == "Heatmap":
            fig, ax = plt.subplots()
            sns.heatmap(results_df.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        elif chart_type == "Scatter Plot":
            fig, ax = plt.subplots()
            sns.scatterplot(data=results_df, x=results_df.columns[0], y=results_df.columns[1], ax=ax)
            st.pyplot(fig)

        # Export results to CSV
        csv_buffer = results_df.to_csv(index=False)
        st.download_button("Download CSV", csv_buffer, "query_results.csv", "text/csv")

    # Query history
    st.markdown("### 🕓 Query History")
    for i, (question, sql_query) in enumerate(st.session_state["query_history"]):
        if st.button(f"Re-run Query {i+1}: {question}"):
            st.session_state["sql_query"] = sql_query
            st.session_state["query_results"] = execute_sql_query(sql_query)

    # Display a dynamic suggestion
    st.markdown("### 💡 Need ideas for queries?")
    st.write(f"**Try this query:** {st.session_state['suggestion']}")
    if st.button("🔄 New Suggestion"):
        generate_prompt_suggestion()  # Generate a new suggestion when the button is clicked

# Run the login page or main application based on authentication
if not st.session_state["is_authenticated"]:
    st.title("🔒 Login Required")
    st.write("Enter the password to access the application.")
    authenticate()
    if st.button("Login"):
        if st.session_state["is_authenticated"]:
            st.success("Authenticated! Please click 'Login' again to proceed.")
else:
    app_interface()

# Generate initial suggestion if not present
if not st.session_state["suggestion"]:
    generate_prompt_suggestion()
