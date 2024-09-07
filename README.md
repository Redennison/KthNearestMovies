# Kth Nearest Movies

![Alt text](./demo-images/demo-image.png)

## Project Overview

This project is a full-stack movie recommendation system that allows users to input a movie from the IMDb Top 250 list and specify the number of similar movies they would like to find. The application uses advanced machine learning techniques to generate movie embeddings based on descriptions and genres, and then leverages the k-Nearest Neighbors (k-NN) algorithm (cosine similarity) to recommend movies most similar to the user's input.

The front end is built with React, where users can input a movie title and the desired number of recommendations. The back end is developed with Flask, where the movie embeddings are precomputed using BERT transformer model for text embeddings and genre information is encoded as categorical features. The recommendations are served in real-time from the Flask API to the React front end.

## How to run

### Frontend

#### Setup
`cd frontend`\
`npm install`

#### Run
`npm start`

### Backend

#### Setup
`cd backend`\
`pip install pandas numpy scikit-learn Flask Flask-CORS`

#### Run
`set FLASK_APP=app.py`\
`flask run`
