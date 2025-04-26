
import streamlit as st
import pandas as pd
import json
import os
import datetime
import html
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
    body {
        background-color: #000000;
        color: #FFFFFF;
    }
    .main-header {
        font-size: 3rem !important;
        color: #60A5FA;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.1);
    }
    .sub-header {
        font-size: 1.8rem !important;
        color: #93C5FD;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #065F46;
        border-left: 5px solid #10B981;
        border-radius: 0.375rem;
        color: white;
    }
    .warning-message {
        padding: 1rem;
        background-color: #92400E;
        border-left: 5px solid #F59E0B;
        border-radius: 0.375rem;
        color: white;
    }
    .book-card {
        background-color: #1F2937;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
        transition: transform 0.3s ease;
        color: white;
    }
    .read-badge {
        background-color: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .unread-badge {
        background-color: #EF4444;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# Helper functions
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
        "read_status": read_status == "Read",
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
            add_book(title, author, year, genre, read_status)

elif nav_options == "View Library":
    st.markdown("<h2 class='sub-header'>Your Library</h2>", unsafe_allow_html=True)
    if st.session_state.library:
        for book in st.session_state.library:
            st.markdown(f"""
            <div class="book-card">
                <h3>{html.escape(book['title'])}</h3>
                <p><strong>Author:</strong> {html.escape(book['author'])}</p>
                <p><strong>Year:</strong> {book.get('year', 'N/A')}</p>
                <p><strong>Genre:</strong> {html.escape(book['genre'])}</p>
                <p><strong>Status:</strong> {"Read" if book['read_status'] else "Unread"}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-message'>Your library is empty. Add books to get started!</div>", unsafe_allow_html=True)

elif nav_options == "Search Books":
    st.markdown("<h2 class='sub-header'>Search Books</h2>", unsafe_allow_html=True)
    search_query = st.text_input("Search by Title or Author")
    if search_query:
        results = [
            book for book in st.session_state.library
            if search_query.lower() in book['title'].lower() or search_query.lower() in book['author'].lower()
        ]
        if results:
            st.markdown("<h3>Search Results:</h3>", unsafe_allow_html=True)
            for book in results:
                st.markdown(f"""
                <div class="book-card">
                    <h3>{html.escape(book['title'])}</h3>
                    <p><strong>Author:</strong> {html.escape(book['author'])}</p>
                    <p><strong>Year:</strong> {book.get('year', 'N/A')}</p>
                    <p><strong>Genre:</strong> {html.escape(book['genre'])}</p>
                    <p><strong>Status:</strong> {"Read" if book['read_status'] else "Unread"}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='warning-message'>No matching books found.</div>", unsafe_allow_html=True)

elif nav_options == "Library Statistics":
    st.markdown("<h2 class='sub-header'>Library Statistics</h2>", unsafe_allow_html=True)
    if st.session_state.library:
        df = pd.DataFrame(st.session_state.library)
        genre_counts = df['genre'].value_counts()
        read_counts = df['read_status'].value_counts()

        st.markdown("### Book Count by Genre")
        fig = px.bar(genre_counts, title="Books by Genre", labels={'index': 'Genre', 'value': 'Count'})
        st.plotly_chart(fig)

        st.markdown("### Read vs Unread Books")
        read_fig = px.pie(read_counts, names=['Unread', 'Read'], title="Read Status")
        st.plotly_chart(read_fig)
    else:
        st.markdown("<div class='warning-message'>Your library is empty. Add books to get statistics!</div>", unsafe_allow_html=True)

# import streamlit as st
# import pandas as pd
# import json
# import os
# import datetime
# import time
# import plotly.express as px
# import plotly.graph_objects as go
# from streamlit_lottie import st_lottie
# import requests

# # Set page configuration
# st.set_page_config(
#     page_title="Personal Library Management System",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         color: #1E3A8A;
#         font-weight: bold;
#         text-align: center;
#     }
#     .sub-header {
#         font-size: 1.8rem;
#         color: #3B82F6;
#         font-weight: 600;
#     }
#     .success-message {
#         background-color: #ECFDF5;
#         border-left: 5px solid #10B981;
#         padding: 1rem;
#         border-radius: 5px;
#     }
#     .warning-message {
#         background-color: #FEF3C7;
#         border-left: 5px solid #F59E0B;
#         padding: 1rem;
#         border-radius: 5px;
#     }
#     .book-card {
#         background-color: #F3F4F6;
#         padding: 1rem;
#         border-radius: 10px;
#         margin-bottom: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Helper functions
# def load_lottieurl(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         return None
#     except:
#         return None

# def load_library():
#     if os.path.exists("library.json"):
#         with open("library.json", "r") as file:
#             return json.load(file)
#     return []

# def save_library(library):
#     with open("library.json", "w") as file:
#         json.dump(library, file)

# # Initialize session state
# if "library" not in st.session_state:
#     st.session_state.library = load_library()

# # Add a book
# def add_book(title, author, year, genre, read_status):
#     book = {
#         "title": title,
#         "author": author,
#         "year": year,
#         "genre": genre,
#         "read_status": read_status,
#         "added_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     st.session_state.library.append(book)
#     save_library(st.session_state.library)
#     st.success("Book added successfully!")

# # Main page
# st.markdown("<h1 class='main-header'>Personal Library Management System</h1>", unsafe_allow_html=True)

# nav_options = st.sidebar.radio(
#     "Navigation",
#     ["View Library", "Add Book", "Search Books", "Library Statistics"]
# )

# if nav_options == "Add Book":
#     st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)
#     with st.form("add_book_form"):
#         title = st.text_input("Title")
#         author = st.text_input("Author")
#         year = st.number_input("Publication Year", min_value=1800, max_value=datetime.datetime.now().year, step=1)
#         genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Romance", "Poetry", "History", "Other"])
#         read_status = st.radio("Read Status", ["Read", "Unread"])
#         submitted = st.form_submit_button("Add Book")
#         if submitted:
#             add_book(title, author, year, genre, read_status == "Read")

# elif nav_options == "View Library":
#     st.markdown("<h2 class='sub-header'>Your Library</h2>", unsafe_allow_html=True)
#     if st.session_state.library:
#         for book in st.session_state.library:
#             st.markdown(f"""
#             <div class="book-card">
#                 <h3>{book['title']}</h3>
#                 <p><strong>Author:</strong> {book['author']}</p>
#                 <p><strong>Year:</strong> {book['year']}</p>
#                 <p><strong>Genre:</strong> {book['genre']}</p>
#                 <p><strong>Status:</strong> {"Read" if book['read_status'] else "Unread"}</p>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.markdown("<div class='warning-message'>Your library is empty. Add books to get started!</div>", unsafe_allow_html=True)
