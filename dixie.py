'''
1. PUT dixie.py AT THE ROOT OF THE FOLDER STRUCTURE YOU WANT TO SEARCH.
2. REPLACE FOLDER NAME "frisky" IN dixie.py WITH THE FOLDER YOU WANT TO SEARCH: SUCH AS "flask".
3. RUN dixie.py.
4. ENTER THE NAMES OF THE FILES YOU WANT TO SEARCH FOR, SEPARATED BY COMMAS (e.g., cont.html, jessie.py, random.js).
'''

import os

def search_files(folder_path, files):
    file_contents = {}
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                file_contents[file] = content
    return file_contents

def write_contents_to_file(file_contents):
    with open('file_contents.txt', 'w') as f:
        for file, content in file_contents.items():
            f.write(f"**{file}:\n{content}\n\n")

def main():
    folder_path = os.path.join(os.getcwd(), 'frisky')
    requested_files = input("Enter the file names (separated by commas): ").split(",")
    requested_files = [file.strip() for file in requested_files]

    file_contents = search_files(folder_path, requested_files)
    write_contents_to_file(file_contents)

    print("File contents have been written to 'file_contents.txt'.")

if __name__ == '__main__':
    main()
