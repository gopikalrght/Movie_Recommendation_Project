const API_BASE = "http://127.0.0.1:5000";

// 1. Fetch and display your saved Watchlist
async function loadWatchlist() {
    const response = await fetch(`${API_BASE}/watchlist/get`);
    const movies = await response.json();
    
    const listElement = document.getElementById("watchlist");
    listElement.innerHTML = ""; // Clear current list
    
    movies.forEach(movie => {
        listElement.innerHTML += `
            <li>
                ${movie.title} (${movie.year})
                <button onclick="deleteMovie('${movie.title}')">Remove</button>
            </li>
        `;
    });
}

// 2. Search for a movie and display it with an "Add" button
async function searchMovie() {
    const query = document.getElementById("searchBar").value;
    const response = await fetch(`${API_BASE}/search?query=${encodeURIComponent(query)}`);
    const results = await response.json();
    
    const resultsDiv = document.getElementById("searchResults");
    resultsDiv.innerHTML = "<h3>Search Results:</h3>";
    
    results.forEach(movie => {
        resultsDiv.innerHTML += `
            <p>
                ${movie.title} (${movie.year}) 
                <button onclick="addMovie('${movie.title}', '${movie.year}')">Add</button>
            </p>
        `;
    });
}

// 3. Add a movie to the database
async function addMovie(title, year) {
    await fetch(`${API_BASE}/watchlist/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title, year: year })
    });
    loadWatchlist(); // Refresh the list
}

// 4. Delete a movie from the database
async function deleteMovie(title) {
    await fetch(`${API_BASE}/watchlist/delete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title })
    });
    loadWatchlist(); // Refresh the list
}

// Initialize the page
loadWatchlist();