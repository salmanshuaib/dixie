'''
1. PUT dixie.py AT THE ROOT OF THE FOLDER STRUCTURE YOU WANT TO SEARCH, I.E. ONE LEVEL ABOVE THE FOLDER YOU WANT TO SEARCH.
2. RUN dixie.py.
3. ENTER THE NAMES OF THE FILES YOU WANT TO SEARCH FOR, SEPARATED BY COMMAS (e.g., cont.html, jessie.py, random.js).
4. A TEXT FILE "file_contents.txt" WILL BE GENERATED THAT YOU CAN USE TO CONVERSE IN CODE WITH ChatGPT.
'''

import os
import tkinter as tk
from tkinter import messagebox

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

def submit_form(event=None):
    """
    Event handler for the form submission.
    Retrieves the folder name, requested file names, performs the file search,
    writes the contents to a file, and displays a success message.
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

    messagebox.showinfo("Success", "File contents have been written to 'file_contents.txt'.")
    window.destroy()

window = tk.Tk()
window.title("File Search")
window.geometry("600x200")  # Adjusted the window size

# Label for folder name entry
folder_label = tk.Label(window, text="Enter the folder name to search in:")
folder_label.pack()

# Entry field for folder name
folder_entry = tk.Entry(window, width=60)
folder_entry.pack(pady=5)

# Label for file names entry
label = tk.Label(window, text="Enter the file names (separated by commas):")
label.pack()

# Entry field for file names
entry = tk.Entry(window, width=60)
entry.pack(pady=10)

# Submit button
submit_button = tk.Button(window, text="Submit", command=submit_form)
submit_button.pack()

# Bind the <Return> key event to the submit_form function
window.bind('<Return>', submit_form)

window.mainloop()
