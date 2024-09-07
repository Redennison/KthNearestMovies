import React, {useState} from 'react'
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import movieTitles from '../data/movie_titles.json'
import Button from '@mui/material/Button';
import MovieBox from '../components/MovieBox';
import Alert from '@mui/material/Alert';
import './HomePage.css';
import _default from '@mui/material/styles/identifier';

const HomePage = () => {
    const [title, setTitle] = useState('');
    const [k, setK] = useState(null)
    const [options, setOptions] = useState([]);
    const [movies, setMovies] = useState([])
    const [error, setError] = useState(null)

    const titleInList = (title) => {
        if (movieTitles.includes(title)) {
            return true
        }
        return false
    }

    const isInteger = (input) => {
        return !isNaN(input)
    }

    const kWithinRange = (k) => {
        return k <= 100
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null)

        if (!titleInList(title)) {
            setError('This movie is not in our database. Please try again with a different movie.')
            return
        }
        
        if (!isInteger(k)) {
            setError('Invalid number of movies. Please try again.')
            return
        }

        if (!kWithinRange(k)) {
            setError('To maintain performance, we do not allow more than 100 similar movies at once. Please try again with a smaller number.')
            return
        }
    
        // Prepare the data to send
        const data = { title, k };
    
        try {
          const response = await fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',  // Specify that you're sending JSON data
            },
            body: JSON.stringify(data),  // Convert data to JSON format
          });
    
          // Handle the response
          const result = await response.json();
          setMovies(result)
        } catch (error) {
            setError(<Alert severity="error">Error occurred. Please try again.</Alert>)
        }
    };
    

    // Update the input value and filter the options based on the input length
    const handleInputChange = (event, newInputValue) => {
        setTitle(newInputValue);

        let filteredOptions = movieTitles.filter(title =>
            title.toLowerCase().includes(newInputValue.toLowerCase())
        );
        
        if (filteredOptions.length > 20) {
            filteredOptions = filteredOptions.slice(0, 20)
        }

        setOptions(filteredOptions);
    };

    return (
        <div className="container">
            <div className="title-container">
                <h1 className="header">Welcome to Kth Nearest Movies</h1>
                <p className="sub-header">This is a proof of concept website that holds data on the top 250 IMBD movie list, and uses machine learning to generate similar movies based on movie genres and descriptions. Input a movie, and type how many of the closest movies you would like to find. The movies are ordered from most similar to least similar.</p>
            </div>
            <div className="form-container">
                <Autocomplete
                    style={{
                        width: '100%',  // Ensure the Autocomplete takes up full width
                        maxWidth: '400px',  // Limit maximum width to 400px if needed
                    }}
                    freeSolo
                    options={options}  // Display the filtered options
                    inputValue={title}  // Track the input value
                    onInputChange={handleInputChange}  // Handle input change
                    renderInput={(params) => (
                        <TextField 
                            {...params} 
                            label="Search movies" 
                            variant="outlined" 
                            style={{ width: '100%' }}  // Ensure the TextField inside takes full width
                        />
                    )}
                />
                <TextField onChange={(e) => setK(e.target.value)} style={{ marginTop: '10px' }} id="outlined-basic" label="Number of movies" variant="outlined" />
                <Button onClick={handleSubmit} style={{ marginTop: '10px', textTransform: 'none', height: '55px', width: '75px' }} className="find-button" variant="contained">Find</Button>
            </div>
            {
                error && (
                    <div style={{ padding: '20px 40px' }}>
                        <Alert severity="error">{error}</Alert>
                    </div>
                )
            }
            <div className="movies-container">
                {movies &&
                    movies.map((movie, index) => (
                        <MovieBox key={index} imageUrl={movie.image} name={movie.name} description={movie.description} />
                    ))
                }
            </div>
        </div>
    )
}

export default HomePage