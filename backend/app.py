from flask import Flask, request, jsonify
from flask_cors import CORS
from ml.ml_functions import find_k_closest_movies

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from other domains (e.g., React frontend)
CORS(app)

# Define the route for handling POST requests at the root URL
# This route will accept a movie title and return the k closest movies
@app.route('/', methods=['POST'])
def get_movies():
    # Extract the JSON data from the incoming request
    data = request.get_json()

    # Extract the 'title' and 'k' parameters from the JSON data
    title = data.get('title')  # Movie title to find similar movies
    k = int(data.get('k'))  # Number of closest movies to return

    # Call the function to find the k closest movies based on the provided title
    k_closest_movies = find_k_closest_movies(title, k)

    # Return the result as a JSON response
    return jsonify(k_closest_movies)

# Run the Flask app in debug mode if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
