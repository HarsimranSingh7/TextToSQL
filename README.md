
---

# Text-to-SQL Application

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://texttosql-p.streamlit.app/)

**Live Demo**: [https://texttosql-p.streamlit.app/](https://texttosql-p.streamlit.app/)

## Overview

The Text-to-SQL Application is an innovative tool designed to bridge the gap between natural language and structured database queries. Using this app, users can input questions in plain English, and the application generates SQL queries that retrieve relevant information from a connected database. This makes data querying more accessible for those unfamiliar with SQL syntax.

This project leverages Streamlit for its front-end, with the backend powered by Google Generative AI to convert natural language inputs into SQL queries.

## Key Features

- **Natural Language to SQL**: Converts English questions into SQL queries, allowing users to interact with databases without SQL knowledge.
- **Data Visualization**: Displays data in various chart formats, including bar charts, line charts, pie charts, heatmaps, and scatter plots.
- **Dynamic Query Suggestions**: Provides users with sample queries to explore different aspects of the database.
- **Secure Access**: Includes a password-protected login screen to ensure only authorized users access the app.
  
## Technologies Used

- **Frontend**: [Streamlit](https://streamlit.io/) for a clean, user-friendly interface.
- **Backend**: [Google Generative AI](https://ai.google/) to transform natural language into SQL queries.
- **Data Visualization**: Matplotlib, Seaborn for various types of data visualizations.
- **Database**: SQLite, with a student performance dataset.

## Getting Started

### Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/TextToSQL.git
   cd TextToSQL
   ```

2. **Set up Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Access the App**

   Once the server starts, open [http://localhost:8501](http://localhost:8501) in your browser.

### Usage

1. **Login**: Use the password provided in the hint on the login screen.
2. **Ask Questions in Plain English**: Enter your question (e.g., "Show the top 5 students with the highest math scores") and the app will generate the corresponding SQL query.
3. **Visualize Data**: Choose from various chart types (bar, line, pie, heatmap, scatter) to visualize your query results.
4. **Explore Suggestions**: Click on the "New Suggestion" button for additional query ideas.

## Example Queries

- "Show students with math scores above 80"
- "List the top 5 students by writing scores"
- "Find the average reading score by gender"
- "Calculate the average math score for students who completed the test preparation course"

## Future Improvements

- **Enhanced NLP Capabilities**: Improve the natural language processing to handle more complex queries.
- **Additional Database Support**: Expand compatibility beyond SQLite.
- **User Management**: Add multi-user support with individual authentication and authorization.

---

