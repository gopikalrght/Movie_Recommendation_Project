const API_BASE = "http://127.0.0.1:5000";

// Load all movies from the watchlist
async function loadWatchlist() {
    try {
        const response = await fetch(`${API_BASE}/watchlist/get`);
        const movies = await response.json();

        const listElement = document.getElementById("watchlist");
        listElement.innerHTML = "";

        if (movies.length === 0) {
            listElement.innerHTML = "<li>No movies in watchlist.</li>";
            return;
        }

        movies.forEach(movie => {
            listElement.innerHTML += `
                <li>
                    ${movie.title} (${movie.year})
                    <button onclick="deleteMovie('${movie.title}')">
                        Remove
                    </button>
                </li>
            `;
        });

    } catch (error) {
        console.error(error);
        alert("Unable to load watchlist.");
    }
}

// Search movies using backend API
async function searchMovie() {
    const query = document.getElementById("searchBar").value.trim();

    if (!query) {
        alert("Please enter a movie name.");
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE}/search?query=${encodeURIComponent(query)}`
        );

        const results = await response.json();

        const resultsDiv = document.getElementById("searchResults");
        resultsDiv.innerHTML = "<h3>Search Results</h3>";

        if (results.length === 0) {
            resultsDiv.innerHTML += "<p>No movies found.</p>";
            return;
        }

        results.forEach(movie => {
            resultsDiv.innerHTML += `
                <p>
                    ${movie.title} (${movie.year})
                    <button onclick="addMovie('${movie.title}','${movie.year}')">
                        Add
                    </button>
                </p>
            `;
        });

    } catch (error) {
        console.error(error);
        alert("Search failed.");
    }
}

// Add movie
async function addMovie(title, year) {
    try {
        await fetch(`${API_BASE}/watchlist/add`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                year: year
            })
        });

        loadWatchlist();

    } catch (error) {
        console.error(error);
        alert("Unable to add movie.");
    }
}

// Delete movie
async function deleteMovie(title) {
    try {
        await fetch(`${API_BASE}/watchlist/delete`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title
            })
        });

        loadWatchlist();

    } catch (error) {
        console.error(error);
        alert("Unable to delete movie.");
    }
}

// Load watchlist when page opens
window.onload = loadWatchlist;