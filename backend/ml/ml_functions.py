import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Function to find the k most similar movies based on embeddings
def find_k_closest_movies(title, k):
    # Load the CSV file containing the movie embeddings and metadata
    # The CSV contains precomputed embeddings and additional information such as movie titles and descriptions
    movies_df = pd.read_csv('./ml/top_250_movies_embeddings.csv')

    # Find the index of the movie with the specified title
    # This assumes that the 'name' column in the DataFrame contains the movie titles
    movie_index = movies_df[movies_df['name'] == title].index[0]

    # Extract the columns that represent the embeddings (numeric columns)
    # These are assumed to be named with digits (e.g., '0', '1', '2', etc.)
    embedding_columns = [col for col in movies_df.columns if col.isdigit()]

    # Retrieve the movie embeddings as a NumPy array
    movie_embeddings = movies_df[embedding_columns].values

    # Get the list of movie titles for reference (from the 'name' column)
    movie_titles = movies_df['name'].values

    # Compute the cosine similarity between the target movie (specified by the title)
    # and all other movies in the dataset. Reshape the target movie's embedding to be compatible with cosine similarity.
    similarities = cosine_similarity(
        movie_embeddings[movie_index].reshape(1, -1), movie_embeddings
    ).flatten()

    # Sort the similarity scores and retrieve the indices of the top k most similar movies
    # The target movie itself is excluded from the results, hence we take the top k after the first result.
    similar_movie_indices = similarities.argsort()[-k-1:-1][::-1]

    # Use the indices to get the corresponding rows (movies) from the DataFrame
    similar_movies_df = movies_df.iloc[similar_movie_indices]

    # Select only the columns containing relevant information: name, description, image, and url
    similar_movies_df = similar_movies_df[['name', 'description', 'image', 'url']]

    # Convert the resulting DataFrame to a list of dictionaries for easy consumption (e.g., by an API)
    similar_movies = similar_movies_df.to_dict(orient='records')

    # Return the list of similar movies
    return similar_movies
