import os
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the SQLite database file
conn = sqlite3.connect('file_search.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS search_history
                  (folder_name TEXT, file_names TEXT)''')
conn.commit()

def search_files(folder_path, files):
    """
    Searches for specified files within a given folder path.
    Returns a dictionary containing the file names as keys and their contents as values.
    """
    file_contents = {}
    for root, _, filenames in os.walk(folder_path):
        for file in filenames:
            if file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    file_contents[file] = content
    return file_contents

def write_contents_to_file(file_contents):
    """
    Writes the contents of the files to a text file named 'file_contents.txt'.
    Each file's content is preceded by the file name.
    """
    with open('file_contents.txt', 'w') as f:
        for file, content in file_contents.items():
            f.write(f"**{file}:\n{content.strip()}")

def save_search_history(folder_name, file_names):
    """
    Saves the folder name and file names to the search_history table in the SQLite database.
    """
    cursor.execute("INSERT INTO search_history VALUES (?, ?)", (folder_name, file_names))
    conn.commit()

def retrieve_last_search():
    """
    Retrieves the last folder name and file names entered from the search_history table.
    Returns a tuple of (folder_name, file_names) or None if no previous search found.
    """
    cursor.execute("SELECT folder_name, file_names FROM search_history ORDER BY ROWID DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row[0], row[1]
    return None

def submit_form(event=None):
    """
    Event handler for the form submission.
    Retrieves the folder name, requested file names, performs the file search,
    writes the contents to a file, saves the search history, and displays a success message.
    """
    folder_name = folder_entry.get()
    folder_path = os.path.join(os.getcwd(), folder_name)
    requested_files = entry.get()
    requested_files = [file.strip() for file in requested_files.split(",")]

    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", f"Folder '{folder_name}' does not exist.")
        return

    file_contents = search_files(folder_path, requested_files)
    write_contents_to_file(file_contents)
    save_search_history(folder_name, ', '.join(requested_files))

    messagebox.showinfo("Success", "File contents have been written to 'file_contents.txt'.")
    window.destroy()

# Retrieve the last search history and pre-fill the form fields
last_search = retrieve_last_search()
if last_search:
    folder_entry_text = last_search[0]
    entry_text = last_search[1]
else:
    folder_entry_text = ""
    entry_text = ""

window = tk.Tk()
window.title("File Search")
window.geometry("600x200")  # Adjusted the window size

# Label for folder name entry
folder_label = tk.Label(window, text="Enter the folder name to search in:")
folder_label.pack()

# Entry field for folder name
folder_entry = tk.Entry(window, width=60)
folder_entry.insert(0, folder_entry_text)
folder_entry.pack(pady=5)

# Label for file names entry
label = tk.Label(window, text="Enter the file names (separated by commas):")
label.pack()

# Entry field for file names
entry = tk.Entry(window, width=60)
entry.insert(0, entry_text)
entry.pack(pady=10)

# Submit button
submit_button = tk.Button(window, text="Submit", command=submit_form)
submit_button.pack()

# Bind the <Return> key event to the submit_form function
window.bind('<Return>', submit_form)

window.mainloop()

# Close the connection to the SQLite database
conn.close()
