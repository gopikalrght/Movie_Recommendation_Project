import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

st.title("🎬 Movie Recommendation System")

# Store search result
if "movie" not in st.session_state:
    st.session_state.movie = None

# ---------------- SEARCH ----------------
st.subheader("🔍 Search Movie")

search_query = st.text_input("Enter movie name")

if st.button("Search"):
    response = requests.get(
        f"{BACKEND_URL}/search",
        params={"query": search_query}
    )

    if response.status_code == 200:
        st.session_state.movie = response.json()
    else:
        st.session_state.movie = None
        st.error("Movie not found.")

# ---------------- DISPLAY MOVIE ----------------
if st.session_state.movie:

    movie = st.session_state.movie

    if movie.get("Poster") and movie["Poster"] != "N/A":
        st.image(movie["Poster"], width=250)

    st.subheader(movie.get("Title", "Unknown"))
    st.write("📅 Year:", movie.get("Year", "N/A"))
    st.write("⭐ IMDb:", movie.get("imdbRating", "N/A"))
    st.write("🎭 Genre:", movie.get("Genre", "N/A"))
    st.write("🎬 Director:", movie.get("Director", "N/A"))
    st.write("👥 Actors:", movie.get("Actors", "N/A"))
    st.write("📝 Plot:")
    st.write(movie.get("Plot", "N/A"))

    if st.button("➕ Add to Watchlist"):

        add = requests.post(
            f"{BACKEND_URL}/watchlist",
            json={
                "title": movie["Title"],
                "year": movie["Year"]
            }
        )

        if add.status_code == 201:
            st.success("Movie added successfully!")
        elif add.status_code == 409:
            st.warning("Movie already exists in watchlist.")
        else:
            try:
                st.error(add.json().get("error", "Failed to add movie"))
            except:
                st.error("Failed to add movie.")

# ---------------- WATCHLIST ----------------
st.subheader("📌 My Watchlist")

response = requests.get(f"{BACKEND_URL}/watchlist")

if response.status_code == 200:

    movies = response.json()

    if movies:
        for m in movies:
            st.write(f"🎬 {m['title']} ({m['year']})")
    else:
        st.info("Watchlist is empty.")

else:
    st.error("Backend not responding.")