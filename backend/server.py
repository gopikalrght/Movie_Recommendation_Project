from flask import Flask, request, jsonify

app = Flask(__name__)

# --- HOME ROUTE ---
@app.route('/')
def home():
    return "Movie Recommendation Backend API is Online!"

# --- TASK 2 ROUTES: USER MANAGEMENT ---
@app.route('/register', methods=['POST'])
def register():
    # Placeholder for registration logic (hashing passwords)
    return jsonify({"message": "Register endpoint is ready!"})

@app.route('/login', methods=['POST'])
def login():
    # Placeholder for login logic (verifying hashes)
    return jsonify({"message": "Login endpoint is ready!"})

# --- TASK 3 ROUTES: RECOMMENDATION ENGINE ---
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    # Placeholder for recommendation logic (filtering movies)
    return jsonify({"movies": ["Inception", "The Dark Knight", "Interstellar"]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)