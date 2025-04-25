# Personal-Library-Manager
This code is a simple web application built using Streamlit to help users manage their personal library. It allows users to add books, view their collection, track reading progress, and even export their library data. Let's break it down into sections and explain what each part does:

1. Imports and Setup
python
Copy
Edit
import streamlit as st
import json
import os
The code starts by importing necessary libraries:

streamlit (st): A library used to create web apps in Python, specifically designed for data science and machine learning.

json: For working with JSON data. This is used to save and load the library data.

os: For checking if the library file exists on the system.

2. Functions to Load and Save Library Data
python
Copy
Edit
def load_library():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            return json.load(f)
    return []
load_library(): This function checks if a file called library.txt exists on the system. If it does, it reads the file and loads the book data into a Python list (in JSON format). If the file doesn't exist, it returns an empty list (meaning there are no books saved yet).

python
Copy
Edit
def save_library(library):
    with open(FILENAME, 'w') as f:
        json.dump(library, f, indent=4)
save_library(): This function saves the current library data (a list of books) into the library.txt file in a JSON format.

3. Streamlit Web App Configuration
python
Copy
Edit
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
st.title("📚 Personal Library Manager")
library = load_library()
st.set_page_config(): Configures the page title and layout of the Streamlit app.

st.title(): Sets the title of the web app to "Personal Library Manager".

library = load_library(): Loads the saved library data from the library.txt file into the library variable.

4. Sidebar Navigation Menu
python
Copy
Edit
menu = ["🏠 Home", "➕ Add Books", "📚 My Library", "📊 Stats", "🔚 Exit / Close App"]
choice = st.sidebar.radio("📌 Navigation", menu)
This block creates a navigation menu on the left sidebar with different options:

Home: The home page of the app.

Add Books: The page where you can add books to the library.

My Library: Displays unread books in the library.

Stats: Shows statistics like the total number of books, read vs unread.

Exit: Exits the app and displays a summary.

5. Adding Books to Library
python
Copy
Edit
if choice == "➕ Add Books":
    st.subheader("➕ Add One or More Books")
    num_books = st.number_input("How many books?", 1, 10, step=1)
The "Add Books" page allows users to input details about the books they want to add (title, author, year, genre, read status).

It first asks how many books they want to add (between 1 and 10).

python
Copy
Edit
with st.form("add_books_form"):
    books_to_add = []
    for i in range(num_books):
        st.markdown(f"**Book {i + 1}**")
        title = st.text_input(f"Title {i+1}", key=f"title_{i}")
        author = st.text_input(f"Author {i+1}", key=f"author_{i}")
        year = st.number_input(f"Year {i+1}", 0, 2100, key=f"year_{i}")
        genre = st.text_input(f"Genre {i+1}", key=f"genre_{i}")
        read = st.radio(f"Read? {i+1}", ["Yes", "No"], key=f"read_{i}")
        books_to_add.append({
            "title": title.strip(),
            "author": author.strip(),
            "year": year,
            "genre": genre.strip(),
            "read": read == "Yes"
        })
Inside the form, the user inputs book details (like title, author, genre, etc.) and submits them.

Each book is stored as a dictionary with these attributes, and these books are added to a list called books_to_add.

python
Copy
Edit
if st.form_submit_button("Add Books"):
    valid_books = [b for b in books_to_add if b["title"] and b["author"] and b["genre"]]
    library.extend(valid_books)
    save_library(library)
    st.success(f"✅ Added {len(valid_books)} book(s) to your library!")
When the form is submitted, valid books (i.e., books with a title, author, and genre) are added to the library list, and the library is saved to the file.

6. Home Page
python
Copy
Edit
elif choice == "🏠 Home":
    st.subheader("📖 Welcome to Your Library")
The Home Page displays a welcome message. If the library is empty, it shows a message saying "Your library is empty". Otherwise, it lists all books and their details (author, year, genre, and read status).

python
Copy
Edit
with st.expander(f"📘 {book['title']}"):
    st.markdown(f"""
    **Author:** {book['author']}  
    **Year:** {book['year']}  
    **Genre:** {book['genre']}  
    **Status:** {'✅ Read' if book['read'] else '📖 Unread'}
    """)
For each book, an expandable section is created to show the book's details. There’s also a button to remove the book from the library.

7. My Library (Unread Books Only)
python
Copy
Edit
elif choice == "📚 My Library":
    st.subheader("📚 Your Unread Books")
The My Library page filters and displays only the books that have not been read yet.

Each unread book can be marked as read using a button, and you can also remove books.

8. Stats (Library Statistics)
python
Copy
Edit
elif choice == "📊 Stats":
    st.subheader("📊 Library Stats")
The Stats page shows statistics, including:

Total number of books.

Number of books read.

Number of unread books.

It also includes a pie chart visualizing the reading progress (read vs unread).

9. Exit / Close App
python
Copy
Edit
elif choice == "🔚 Exit / Close App":
    st.markdown("## 🔚 Exit / Close App")
    st.markdown("### 📊 Your Library Summary")
The Exit page shows a summary of the user's library, including the number of books read and unread.

There’s also an option to export the library as a JSON file and a motivational quote.

10. Miscellaneous Features
st.balloons(): A fun touch that displays virtual balloons when the user exits the app.

st.download_button(): Provides an option for users to download their library as a JSON file.

Summary:
In essence, this code is a simple and interactive personal library manager. It allows users to:

Add books to their library.

Track which books have been read and which ones are unread.

View stats about their library.

Remove books from their collection.

Export their library data to a JSON file.

This app uses Streamlit to create an intuitive, user-friendly interface for managing personal reading collections.
