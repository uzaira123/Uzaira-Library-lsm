import streamlit as st
import pandas as pd
import json
import os
import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Set page configuration
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        font-weight: bold;
        text-align: center;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #3B82F6;
        font-weight: 600;
    }
    .success-message {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        padding: 1rem;
        border-radius: 5px;
    }
    .warning-message {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 1rem;
        border-radius: 5px;
    }
    .book-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def load_lottieurl(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def load_library():
    if os.path.exists("library.json"):
        with open("library.json", "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open("library.json", "w") as file:
        json.dump(library, file)

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Add a book
def add_book(title, author, year, genre, read_status):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status,
        "added_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library(st.session_state.library)
    st.success("Book added successfully!")

# Main page
st.markdown("<h1 class='main-header'>Personal Library Management System</h1>", unsafe_allow_html=True)

nav_options = st.sidebar.radio(
    "Navigation",
    ["View Library", "Add Book", "Search Books", "Library Statistics"]
)

if nav_options == "Add Book":
    st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1800, max_value=datetime.datetime.now().year, step=1)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "Poetry", "History", "Other"])
        read_status = st.radio("Read Status", ["Read", "Unread"])
        submitted = st.form_submit_button("Add Book")
        if submitted:
            add_book(title, author, year, genre, read_status == "Read")

elif nav_options == "View Library":
    st.markdown("<h2 class='sub-header'>Your Library</h2>", unsafe_allow_html=True)
    if st.session_state.library:
        for book in st.session_state.library:
            st.markdown(f"""
            <div class="book-card">
                <h3>{book['title']}</h3>
                <p><strong>Author:</strong> {book['author']}</p>
                <p><strong>Year:</strong> {book['year']}</p>
                <p><strong>Genre:</strong> {book['genre']}</p>
                <p><strong>Status:</strong> {"Read" if book['read_status'] else "Unread"}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-message'>Your library is empty. Add books to get started!</div>", unsafe_allow_html=True)
