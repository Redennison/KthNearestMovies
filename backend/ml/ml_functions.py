import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Takes a movie title & # of movies, returns a list containing kth most similar movies
def find_k_closest_movies(title, k):
    # Load csv file
    movies_df = pd.read_csv('./ml/top_250_movies_embeddings.csv')

    movie_index = movies_df[movies_df['name'] == title].index[0]

    # Extract the embedding columns
    embedding_columns = [col for col in movies_df.columns if col.isdigit()]

    # Get the embeddings as a NumPy array
    movie_embeddings = movies_df[embedding_columns].values

    # Get the movie titles for reference
    movie_titles = movies_df['name'].values

    # Compute cosine similarity between the target movie and all other movies
    similarities = cosine_similarity(
        movie_embeddings[movie_index].reshape(1, -1), movie_embeddings
    ).flatten()

    # Get the indices of the top k most similar movies (excluding the movie itself)
    similar_movie_indices = similarities.argsort()[-k-1:-1][::-1]

    similar_movies_df = movies_df.iloc[similar_movie_indices]
    similar_movies_df = similar_movies_df[['name', 'description', 'image', 'url']]

    similar_movies = similar_movies_df.to_dict(orient='records')

    return similar_movies
