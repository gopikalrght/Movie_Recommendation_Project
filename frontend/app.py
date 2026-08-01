import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_poster(movie):
    poster = movie.get("Poster") or movie.get("poster")

    if poster and poster != "N/A":
        return poster

    return None


def get_title(movie):
    return movie.get("Title") or movie.get("title") or "Unknown"


def get_year(movie):
    return movie.get("Year") or movie.get("year") or "N/A"


def get_imdb_id(movie):
    return movie.get("imdbID") or movie.get("imdb_id") or movie.get("imdbId")


def normalize_movies(data):
    """
    Converts backend responses into a list of movie dictionaries.
    """

    if isinstance(data, list):
        return [
            movie for movie in data
            if isinstance(movie, dict)
        ]

    if isinstance(data, dict):

        # Some APIs return {"Search": [...]}
        if isinstance(data.get("Search"), list):
            return [
                movie for movie in data["Search"]
                if isinstance(movie, dict)
            ]

        # Single movie object
        return [data]

    return []


def search_movies(query):
    try:
        response = requests.get(
            f"{BACKEND_URL}/search",
            params={"query": query},
            timeout=10
        )

        if response.status_code == 200:
            return normalize_movies(response.json())

        return []

    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection error: {e}")
        return []


def add_to_watchlist(movie):

    data = {
        "title": get_title(movie),
        "year": get_year(movie),
        "poster": get_poster(movie) or "N/A",
        "imdbID":get_imdb_id(movie)
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/watchlist",
            json=data,
            timeout=10
        )

        if response.status_code == 201:
            st.success("✅ Movie added to watchlist!")
            return

        if response.status_code == 409:
            st.warning("⚠️ Movie already exists in watchlist.")
            return

        try:
            error = response.json().get(
                "error",
                "Failed to add movie"
            )
        except Exception:
            error = "Failed to add movie"

        st.error(error)

    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection error: {e}")


def load_recommendations(title):

    try:
        response = requests.get(
            f"{BACKEND_URL}/recommendations",
            params={"title": title},
            timeout=10
        )

        if response.status_code == 200:
            return normalize_movies(response.json())

        return []

    except requests.exceptions.RequestException:
        return []


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🎬 Movie Recommendation System")

st.write(
    "Search for a movie, explore its details, "
    "add it to your watchlist, and discover similar movies."
)


# =========================================================
# SEARCH
# =========================================================

st.subheader("🔍 Search Movie")

search_query = st.text_input(
    "Enter movie name",
    placeholder="Example: Batman"
)

if st.button("🔎 Search", use_container_width=True):

    if not search_query.strip():
        st.warning("Please enter a movie name.")
    else:

        with st.spinner("Searching movies..."):

            results = search_movies(search_query.strip())

        if results:
            st.session_state.search_results = results
            st.session_state.selected_movie = None
            st.session_state.recommendations = []

        else:
            st.session_state.search_results = []
            st.error("Movie not found.")


# =========================================================
# SEARCH RESULTS
# =========================================================

if st.session_state.search_results:

    st.subheader("🎞️ Search Results")

    results = st.session_state.search_results

    # Display movies in rows of 4
    for start in range(0, len(results), 4):

        row = results[start:start + 4]

        columns = st.columns(4)

        for column, movie in zip(columns, row):

            with column:

                poster = get_poster(movie)

                if poster:
                    st.image(
                        poster,
                        use_container_width=True
                    )
                else:
                    st.write("🎬 No poster")

                st.markdown(
                    f"### {get_title(movie)}"
                )

                st.write(
                    f"📅 {get_year(movie)}"
                )

                imdb_id = get_imdb_id(movie)

                if imdb_id:
                    st.caption(
                        f"IMDb: {imdb_id}"
                    )

                if st.button(
                    "View Details",
                    key=f"details_{imdb_id}_{get_title(movie)}"
                ):

                    imdb_id = get_imdb_id(movie)

                    details = requests.get(
                       f"{BACKEND_URL}/movie/{imdb_id}"
                    )

                    if details.status_code == 200:
                        st.session_state.selected_movie = details.json()
                    else:
                        st.session_state.selected_movie = movie

                    st.session_state.recommendations = load_recommendations(
                        get_title(st.session_state.selected_movie)
                    )

                    st.rerun()


# =========================================================
# SELECTED MOVIE
# =========================================================

movie = st.session_state.selected_movie

if movie:

    st.divider()

    st.subheader("🎬 Movie Details")

    col1, col2 = st.columns([1, 2])

    # -----------------------------------------------------
    # POSTER
    # -----------------------------------------------------

    with col1:

        poster = get_poster(movie)

        if poster:
            st.image(
                poster,
                use_container_width=True
            )
        else:
            st.write("🎬 Poster not available")


    # -----------------------------------------------------
    # DETAILS
    # -----------------------------------------------------

    with col2:

        st.title(
            get_title(movie)
        )

        st.write(
            f"📅 **Year:** {get_year(movie)}"
        )

        st.write(
            f"⭐ **IMDb Rating:** "
            f"{movie.get('imdbRating', 'N/A')}"
        )

        st.write(
            f"🎭 **Genre:** "
            f"{movie.get('Genre', 'N/A')}"
        )

        st.write(
            f"🎬 **Director:** "
            f"{movie.get('Director', 'N/A')}"
        )

        st.write(
            f"👥 **Actors:** "
            f"{movie.get('Actors', 'N/A')}"
        )

        st.write(
            f"⏱️ **Runtime:** "
            f"{movie.get('Runtime', 'N/A')}"
        )

        st.write(
            f"🌍 **Language:** "
            f"{movie.get('Language', 'N/A')}"
        )

        st.write("📝 **Plot:**")

        st.write(
            movie.get("Plot", "N/A")
        )

        imdb_id = get_imdb_id(movie)

        if imdb_id:
            st.write(
                f"🆔 **IMDb ID:** {imdb_id}"
            )

        if st.button(
            "➕ Add to Watchlist",
            key=f"add_search_{get_imdb_id(movie)}"
        ):
            add_to_watchlist(movie)
        




# =========================================================
# RECOMMENDATIONS
# =========================================================

if movie:

    st.divider()

    st.subheader("🎬 Recommended Movies")

    recommendations = st.session_state.recommendations

    if recommendations:

        for start in range(
            0,
            len(recommendations),
            4
        ):

            row = recommendations[start:start + 4]

            columns = st.columns(4)

            for column, recommendation in zip(
                columns,
                row
            ):

                with column:

                    poster = get_poster(
                        recommendation
                    )

                    if poster:

                        st.image(
                            poster,
                            use_container_width=True
                        )

                    st.markdown(
                        f"### {get_title(recommendation)}"
                    )

                    st.write(
                        f"📅 {get_year(recommendation)}"
                    )

                    imdb_id = get_imdb_id(
                        recommendation
                    )

                    if imdb_id:

                        st.caption(
                            f"IMDb: {imdb_id}"
                        )

                    if st.button(
                        "View Details",
                        key=f"recommend_{imdb_id}_{get_title(recommendation)}"
                    ):

                        imdb_id = get_imdb_id(recommendation)

                        details = requests.get(
                            f"{BACKEND_URL}/movie/{imdb_id}"
                        )

                        if details.status_code == 200:
                            st.session_state.selected_movie = details.json()
                        else:
                            st.session_state.selected_movie = recommendation

                        st.session_state.recommendations = load_recommendations(
                            get_title(st.session_state.selected_movie)
                        )

                        st.rerun()

    else:

        st.info(
            "No recommendations available."
        )


# =========================================================
# WATCHLIST
# =========================================================

st.divider()

st.subheader("📌 My Watchlist")

try:

    response = requests.get(
        f"{BACKEND_URL}/watchlist",
        timeout=10
    )

    if response.status_code == 200:

        watchlist = normalize_movies(
            response.json()
        )

        if watchlist:

            for movie_item in watchlist:

                col1, col2 = st.columns(
                    [1, 4]
                )

                # -------------------------------------------------
                # WATCHLIST POSTER
                # -------------------------------------------------

                with col1:

                    poster = get_poster(
                        movie_item
                    )

                    if poster:

                        st.image(
                            poster,
                            width=130
                        )

                    else:

                        st.write(
                            "🎬 No poster"
                        )

                # -------------------------------------------------
                # WATCHLIST DETAILS
                # -------------------------------------------------

                with col2:

                    title = get_title(
                        movie_item
                    )

                    year = get_year(
                        movie_item
                    )

                    st.markdown(
                        f"### {title}"
                    )

                    st.write(
                        f"📅 Year: {year}"
                    )

                    if st.button(
                        "❌ Remove",
                        key=f"remove_{title}_{year}"
                    ):

                        try:

                            delete_response = requests.delete(
                                f"{BACKEND_URL}/watchlist/{title}",
                                timeout=10
                            )

                            if delete_response.status_code == 200:

                                st.success(
                                    "Movie removed."
                                )

                                st.rerun()

                            else:

                                st.error(
                                    "Failed to remove movie."
                                )

                        except requests.exceptions.RequestException as e:

                            st.error(
                                f"Backend error: {e}"
                            )

                st.divider()

        else:

            st.info(
                "Watchlist is empty."
            )

    else:

        st.error(
            "Unable to load watchlist."
        )

except requests.exceptions.RequestException as e:

    st.error(
        f"Backend not responding: {e}"
    )