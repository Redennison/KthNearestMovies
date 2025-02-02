# -*- coding: utf-8 -*-
"""
movie_recommendation.ipynb

Automatically generated by Colab.
"""

import torch
from google.colab import drive
from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer

# Load the movie dataset (Top 250 movies from IMDb)
movies_csv = 'top_250_movies.csv'
movies_df = pd.read_csv(movies_csv)

# Load pre-trained BERT model and tokenizer for generating embeddings from movie descriptions
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  # Initialize BERT tokenizer
model = BertModel.from_pretrained('bert-base-uncased')  # Initialize BERT model

# Set model to evaluation mode, as we're not training it, just generating embeddings
model.eval()

# Extract the movie descriptions from the DataFrame as a list of strings
descriptions = movies_df['description'].astype(str).tolist()

# Define a function to generate BERT embeddings in batches for efficiency
# This function takes movie descriptions and generates embeddings in batches (to avoid memory issues)
def get_embeddings_batch(descriptions, batch_size=32):
    embeddings = []  # List to store embeddings
    for i in range(0, len(descriptions), batch_size):
        # Get the current batch of descriptions
        batch_descriptions = descriptions[i:i+batch_size]
        
        # Tokenize the batch of descriptions for input to the BERT model
        encoded_inputs = tokenizer(batch_descriptions, return_tensors='pt', padding=True, truncation=True, max_length=128)

        # Run the tokenized inputs through BERT to get the embeddings
        with torch.no_grad():  # No need for gradient calculation (we're not training)
            outputs = model(**encoded_inputs)

        # Extract the CLS token (first token) embeddings for each description
        cls_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        embeddings.append(cls_embeddings)

        # Print progress information for the current batch
        print(f'batch {(i)/batch_size+1} of {len(descriptions)/batch_size} completed')

    # Concatenate all batch embeddings into a single NumPy array
    embeddings = np.vstack(embeddings)
    return embeddings

# Generate BERT embeddings for all movie descriptions
batch_embeddings = get_embeddings_batch(descriptions, batch_size=32)

# Initialize MultiLabelBinarizer to convert movie genres into one-hot encoded format
mlb = MultiLabelBinarizer()

# Split the 'genre' column of movies_df into a list of genres for each movie
movies_df['categories_split'] = movies_df['genre'].apply(lambda x: x.split(', '))

# One-hot encode the genre categories using the MultiLabelBinarizer
categories_one_hot = mlb.fit_transform(movies_df['categories_split'])

# Convert the one-hot encoded genres into a DataFrame for easy manipulation
categories_df = pd.DataFrame(categories_one_hot, columns=mlb.classes_)

# Combine the BERT-generated description embeddings with the one-hot encoded genre data
combined_features = np.concatenate([batch_embeddings, categories_df.values], axis=1)

# Create a new DataFrame to store the combined features and other metadata (movie name, description, image, url)
combined_df = pd.DataFrame(combined_features)

# Add the movie metadata (name, description, image, url) to the combined DataFrame
combined_df['name'] = movies_df['name']
combined_df['description'] = movies_df['description']
combined_df['image'] = movies_df['image']
combined_df['url'] = movies_df['url']

# Mount Google Drive to save the final combined data
drive.mount('/content/drive')

# Save the final DataFrame containing movie features and metadata to a CSV file in Google Drive
combined_df.to_csv('/content/drive/My Drive/top_250_movie_data.csv', index=False)
