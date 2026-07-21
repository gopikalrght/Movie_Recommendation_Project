import streamlit as st
import requests

st.title("🎬 Movie Recommendation System")

movie = st.text_input("Enter Movie Name")
year = st.text_input("Enter Year")

if st.button("Add Movie"):
    if movie and year:
        response = requests.post(
            "http://127.0.0.1:5000/watchlist",
            json={"title": movie, "year": int(year)}
        )

        if response.status_code == 201:
            st.success("Movie added successfully!")
        else:
            st.error(response.json().get("error", "Failed to add movie"))
    else:
        st.warning("Please enter movie and year")
st.subheader("📌 My Watchlist")

response = requests.get("http://127.0.0.1:5000/watchlist")

if response.status_code == 200:
    movies = response.json()
    for m in movies:
        st.write(f"🎬 {m['title']} ({m['year']})")
else:
    st.error("Backend not responding")


