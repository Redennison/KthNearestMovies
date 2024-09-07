import React, { useState } from 'react'
import './MovieBox.css'

const MovieBox = ({ name, description, imageUrl }) => {
    const [isHovered, setIsHovered] = useState(false);

    return (
        <div
            className="movie-container"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >   
            {
                !isHovered ? (
                    <img src={imageUrl} alt="Image" className="image-card__image" />
                ) : (
                    <div>
                        <h2>{name}</h2>
                        <p style={{ paddingLeft: '10px', paddingRight: '10px' }}>
                            
                            {description}
                        </p>
                    </div>
                )
            }
        </div>
    )
}

export default MovieBox