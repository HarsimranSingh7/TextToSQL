import os
import kaggle
import sqlite3
import pandas as pd

# Kaggle dataset details
dataset = "spscientist/students-performance-in-exams"
csv_file = "StudentsPerformance.csv"  # The name of the CSV file in the downloaded dataset
db_file = "student.db"  # The SQLite database file to create or use

# Step 1: Download the dataset if not already downloaded
if not os.path.exists(csv_file):
    print("Downloading dataset from Kaggle...")
    kaggle.api.dataset_download_files(dataset, path=".", unzip=True)
    print(f"Dataset downloaded and extracted to the current directory as {csv_file}.")
else:
    print("Dataset already exists.")

# Step 2: Load the dataset into an SQLite database
print("Loading dataset into SQLite database...")

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Rename columns to match your database schema, if necessary
# Adjust these column names to match the CSV data structure
df.rename(columns={
    "gender": "GENDER",
    "race/ethnicity": "ETHNICITY",
    "parental level of education": "PARENT_EDUCATION",
    "lunch": "LUNCH",
    "test preparation course": "PREP_COURSE",
    "math score": "MATH_SCORE",
    "reading score": "READING_SCORE",
    "writing score": "WRITING_SCORE"
}, inplace=True)

# Connect to the SQLite database (it will create student.db if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the STUDENT table with appropriate columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS STUDENT (
        GENDER TEXT,
        ETHNICITY TEXT,
        PARENT_EDUCATION TEXT,
        LUNCH TEXT,
        PREP_COURSE TEXT,
        MATH_SCORE INTEGER,
        READING_SCORE INTEGER,
        WRITING_SCORE INTEGER
    )
''')

# Insert data into the STUDENT table
df.to_sql("STUDENT", conn, if_exists="replace", index=False)

# Commit and close the connection
conn.commit()
conn.close()

print(f"Data loaded successfully from {csv_file} to {db_file} SQLite database.")
