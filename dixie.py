'''
1. PUT dixie.py AT THE ROOT OF THE FOLDER STRUCTURE YOU WANT TO SEARCH, I.E. ONE LEVEL ABOVE THE FOLDER YOU WANT TO SEARCH.
2. REPLACE FOLDER NAME "frisky" IN dixie.py WITH THE FOLDER YOU WANT TO SEARCH: SUCH AS "flask".
3. RUN dixie.py.
4. ENTER THE NAMES OF THE FILES YOU WANT TO SEARCH FOR, SEPARATED BY COMMAS (e.g., cont.html, jessie.py, random.js).
5. A TEXT FILE "file_contents.txt" WILL BE GENERATED THAT YOU CAN USE TO CONVERSE IN CODE WITH ChatGPT.
'''


import os
import tkinter as tk
from tkinter import messagebox

def search_files(folder_path, files):
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
    with open('file_contents.txt', 'w') as f:
        for file, content in file_contents.items():
            f.write(f"**{file}:\n{content}\n\n")

def submit_form():
    folder_path = os.path.join(os.getcwd(), 'flask')
    requested_files = entry.get()
    requested_files = [file.strip() for file in requested_files.split(",")]

    file_contents = search_files(folder_path, requested_files)
    write_contents_to_file(file_contents)

    messagebox.showinfo("Success", "File contents have been written to 'file_contents.txt'.")
    window.destroy()

window = tk.Tk()
window.title("File Search")
window.geometry("600x200")  # Adjusted the window size

label = tk.Label(window, text="Enter the file names (separated by commas):")
label.pack()

entry = tk.Entry(window, width=60)
entry.pack(pady=20)

submit_button = tk.Button(window, text="Submit", command=submit_form)
submit_button.pack()

window.mainloop()
