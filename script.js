function addMovie() {
    const movie = document.getElementById('movieName').value;
    const year = document.getElementById('year').value;

    const movieData = {
        name: movie,
        year: year
    };

    fetch('http://127.0.0.1:5000/watchlist/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(movieData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('movieName').value = '';
        document.getElementById('year').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to connect to the server.');
    });
}