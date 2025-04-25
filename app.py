import streamlit as st
import json
import os

FILENAME = "library.txt"

# ---------- Functions to load/save data ---------- #
def load_library():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            return json.load(f)
    return []

def save_library(library):
    with open(FILENAME, 'w') as f:
        json.dump(library, f, indent=4)

# ---------- Setup ---------- #
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
st.title("📚 Personal Library Manager")
library = load_library()

# ---------- Menu ---------- #
menu = ["🏠 Home", "➕ Add Books", "📚 My Library", "📊 Stats", "🔚 Exit / Close App"]
choice = st.sidebar.radio("📌 Navigation", menu)

# ---------- Add Books ---------- #
if choice == "➕ Add Books":
    st.subheader("➕ Add One or More Books")
    num_books = st.number_input("How many books?", 1, 10, step=1)

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

        if st.form_submit_button("Add Books"):
            valid_books = [b for b in books_to_add if b["title"] and b["author"] and b["genre"]]
            library.extend(valid_books)
            save_library(library)
            st.success(f"✅ Added {len(valid_books)} book(s) to your library!")

# ---------- Home ---------- #
elif choice == "🏠 Home":
    st.subheader("📖 Welcome to Your Library")

    if not library:
        st.info("📭 Your library is empty.")
    else:
        st.markdown("### 📚 Click a book to see its details and actions:")
        updated_library = library.copy()

        for i, book in enumerate(library):
            with st.expander(f"📘 {book['title']}"):
                st.markdown(f"""
                **Author:** {book['author']}  
                **Year:** {book['year']}  
                **Genre:** {book['genre']}  
                **Status:** {'✅ Read' if book['read'] else '📖 Unread'}
                """)

                # Remove button with unique key
                if st.button(f"🗑️ Remove '{book['title']}'", key=f"remove_{i}"):
                    updated_library = [b for b in library if b != book]
                    save_library(updated_library)
                    st.success(f"✅ '{book['title']}' has been removed from your library.")
                    st.cache_data.clear()
                    

# ---------- My Library (Unread Books Only) ---------- #
elif choice == "📚 My Library":
    st.subheader("📚 Your Unread Books")
    unread_books = [b for b in library if not b["read"]]

    if not unread_books:
        st.success("🎉 You've read all your books!")
    else:
        updated_library = library.copy()
        for book in unread_books:
            query = f"{book['title']} {book['author']}".replace(" ", "+")
            google_link = f"https://www.google.com/search?q={query}+book"

            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### 📘 [{book['title']}]({google_link})")
                st.markdown(f"""
                - **Author:** {book['author']}  
                - **Year:** {book['year']}  
                - **Genre:** {book['genre']}  
                - **Status:** 📖 Unread
                """)
            with col2:
                if st.button("✅ Mark as Read", key=f"read_{book['title']}"):
                    for b in updated_library:
                        if b["title"] == book["title"]:
                            b["read"] = True
                            break
                    save_library(updated_library)
                    st.success(f"✅ '{book['title']}' marked as read!")
                    st.experimental_rerun()

        # Remove manually
        st.divider()
        to_remove = st.selectbox("🗑️ Remove a book", ["None"] + [b["title"] for b in unread_books])
        if to_remove != "None":
            updated_library = [b for b in updated_library if b["title"] != to_remove]
            save_library(updated_library)
            st.success(f"🗑️ '{to_remove}' removed.")
            st.experimental_rerun()

# ---------- Stats ---------- #
elif choice == "📊 Stats":
    st.subheader("📊 Library Stats")
    total = len(library)
    read_count = sum(b['read'] for b in library)
    unread_count = total - read_count

    if total == 0:
        st.info("📭 Library is empty.")
    else:
        col1, col2 = st.columns(2)
        col1.metric("Total Books", total)
        col2.metric("Books Read", read_count)
        st.metric("Unread", unread_count)

        import matplotlib.pyplot as plt  # type: ignore
        fig, ax = plt.subplots()
        ax.pie([read_count, unread_count], labels=["Read", "Unread"], autopct="%1.1f%%", startangle=90, colors=["#2ecc71", "#e74c3c"])
        ax.axis("equal")
        st.markdown("### 📈 Reading Progress")
        st.pyplot(fig)

# ---------- Exit ---------- #
elif choice == "🔚 Exit / Close App":
    st.markdown("## 🔚 Exit / Close App")
    st.markdown("---")

    total_books = len(library)
    read_books = sum(b['read'] for b in library)
    unread_books = total_books - read_books

    # Quote for motivation
    st.markdown("### 📖 *“A reader lives a thousand lives before he dies . . . The man who never reads lives only one.”*")
    st.markdown("<div style='text-align: right;'>— Qandeel Fatima</div>", unsafe_allow_html=True)

    # Session summary
    st.markdown("### 📊 Your Library Summary")
    st.write(f"- **Total books:** {total_books}")
    st.write(f"- ✅ **Books read:** {read_books}")
    st.write(f"- 📖 **Books unread:** {unread_books}")

    # Export button
    st.markdown("### 📁 Export Your Library")
    json_data = json.dumps(library, indent=4)
    st.download_button("⬇️ Download Library as JSON", json_data, file_name="my_library_backup.json")

    # Credits & next steps
    st.markdown("---")
    st.markdown("### 💡 Tips Before You Go")
    st.markdown("""
    - Come back and keep your reading progress updated.  
    - Explore new genres and revisit your old favorites.  
    - Share this app with fellow book lovers! 📚💬
    """)

    st.markdown("### ✨ Thank You for Using *Personal Library Manager*!")
    st.markdown("Made by ❤️ Qandeel Fatima")

    # Optional fun touch
    st.balloons()

    # End app
    st.stop()

