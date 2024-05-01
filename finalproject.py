import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tabulate import tabulate
import pandas as pd
import mysql.connector
from mysql.connector import Error

try:
    import mysql.connector
    print("mysql-connector-python is installed.")
except ImportError:
    print("mysql-connector-python is NOT installed.")

def insert_data_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel("file_path")
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = conn.cursor()
            for index, row in df.iterrows():
                # Apply constraints before inserting data into the database
                if (row['consent'] == "I Agree" and 
                    row['duration'] > 60 and 
                    row['finished'] and 
                    row['progress'] == 100 and 
                    row['citizenship'] == "United States of America" and 
                    row['pet'].lower() == "fluffy" and 
                    2024 - int(row['birth_year']) >= 18 and 
                    len(str(row['surroundings']).split()) >= 8):
                    
                    # All constraints are satisfied, proceed with insertion
                    sql = "INSERT INTO ParticipantData (consent, duration, end_date, finished, progress, gender, citizenship, years_in_usa, school, education_level, parent_education, employment, household_inc, household_size, household_under_18, political_party, birth_year, political_orientation, religious, religious_group, pet, surroundings, hispanic, race_american_native, race_asian, race_black, race_pacific, race_white, race_none, marital, english_first, english_skill, home_lang, home_lang_other, zip_code, recorded_date, response_id, start_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = tuple(str(value) for value in row)
                    cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            print("Data inserted successfully!")
        except Error as e:
            print(f"Error: {e}")

def clear_database():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        sql = "DELETE FROM ParticipantData"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database cleared successfully!")
    except Error as e:
        print(f"Error: {e}")

def display_results(cursor, results):
    result_window = tk.Toplevel(root)
    result_window.title("Query Results")

    # Use scrolledtext for scrolling
    result_text = scrolledtext.ScrolledText(result_window, height=20, width=80, wrap=tk.NONE)
    result_text.pack(padx=10, pady=10)

    # Print tabulated results
    headers = [description[0] for description in cursor.description]
    table = tabulate(results, headers=headers, tablefmt="pretty")
    result_text.insert(tk.END, table)

    result_text.config(state=tk.DISABLED)

def execute_custom_sql():
    sql_statement = custom_sql_entry.get("1.0", tk.END).strip()
    if sql_statement:
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            
            # If the query returns results, fetch and display them
            if cursor.description is not None:
                results = cursor.fetchall()
                display_results(cursor, results)  # Pass cursor as argument
                
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Custom SQL statement executed successfully!")
        except Error as e:
            messagebox.showerror("Error", f"Error: {e}")
    else:
        messagebox.showwarning("Warning", "Please enter a SQL statement.")


# Define your MySQL connection parameters
host = "cps-database.gonzaga.edu"
user = "bberton"
password = "bberton10842735"
database = "bberton_DB"

# Create the tkinter GUI window
root = tk.Tk()
root.title("MySQL Data Manipulation: Table 'ParticipantData'")

# Button to select and insert data from file
insert_button = tk.Button(root, text="Insert Data from File", command=insert_data_from_file)
insert_button.pack(pady=10)

# Button to clear the database
clear_button = tk.Button(root, text="Clear Database", command=clear_database)
clear_button.pack(pady=10)

# Entry and button for custom SQL statement
custom_sql_entry = tk.Text(root, height=5, width=50)
custom_sql_entry.pack(pady=10)
custom_sql_button = tk.Button(root, text="Execute Custom SQL", command=execute_custom_sql)
custom_sql_entry.insert(tk.END, "SELECT * FROM ParticipantData;")
custom_sql_button.pack(pady=5)

# Run the tkinter main loop
root.mainloop()