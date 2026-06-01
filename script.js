// Function to fetch and display the list
async function fetchWatchlist() {
    const response = await fetch('http://127.0.0.1:5000/watchlist');
    const movies = await response.json();
    
    const list = document.getElementById('watchlist');
    list.innerHTML = ''; // Clear current list

    movies.forEach(movie => {
        const li = document.createElement('li');
        li.textContent = `${movie.title} (${movie.year})`;
        list.appendChild(li);
    });
}

// Function to add a movie and refresh the view
async function addMovie() {
    const title = document.getElementById('movieTitle').value;
    const year = document.getElementById('movieYear').value;

    const response = await fetch('http://127.0.0.1:5000/watchlist/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: title, year: year })
    });

    const result = await response.json();
    alert(result.message);
    
    // Refresh the list after adding
    fetchWatchlist();
}

// Load the list when the page opens
fetchWatchlist();