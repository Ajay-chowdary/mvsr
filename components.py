import streamlit as st
import base64
from PIL import Image
import io

def movie_card(title, poster_url, rating=None, year=None, genres=None, movie_id=None):
    """
    Create a movie card with hover effects.
    
    Args:
        title (str): Movie title
        poster_url (str): URL to the movie poster
        rating (float, optional): Movie rating
        year (int, optional): Release year
        genres (list, optional): List of genres
        movie_id (int, optional): Movie ID for linking
        
    Returns:
        str: HTML for the movie card
    """
    # Format rating with stars
    rating_html = ""
    if rating:
        stars = int(rating / 2)  # Convert 10-point scale to 5-star scale
        rating_html = f"""
            <div class="movie-rating">
                <span class="rating-star">{'★' * stars}{'☆' * (5-stars)}</span>
                <span>{rating}/10</span>
            </div>
        """
    
    # Format genres
    genres_html = ""
    if genres:
        genres_html = f"""
            <div class="movie-genres">
                {', '.join(genres[:3])}
            </div>
        """
    
    # Format year
    year_html = f"<div class='movie-year'>{year}</div>" if year else ""
    
    # Create the card HTML
    card_html = f"""
        <div class="movie-card fade-in">
            <img class="movie-poster" src="{poster_url}" alt="{title}">
            <div class="movie-info">
                <div class="movie-title">{title}</div>
                {rating_html}
                {year_html}
                {genres_html}
            </div>
        </div>
    """
    
    return card_html

def actor_card(name, image_url, role=None, actor_id=None):
    """
    Create an actor card with hover effects.
    
    Args:
        name (str): Actor name
        image_url (str): URL to the actor's image
        role (str, optional): Role in the movie
        actor_id (int, optional): Actor ID for linking
        
    Returns:
        str: HTML for the actor card
    """
    role_html = f"<div class='actor-role'>{role}</div>" if role else ""
    
    card_html = f"""
        <div class="actor-card fade-in">
            <img class="actor-image" src="{image_url}" alt="{name}">
            <div class="actor-name">{name}</div>
            {role_html}
        </div>
    """
    
    return card_html

def hero_section(title, subtitle=None, background_image=None):
    """
    Create a hero section with a title and optional subtitle.
    
    Args:
        title (str): Main title
        subtitle (str, optional): Subtitle text
        background_image (str, optional): URL to background image
        
    Returns:
        str: HTML for the hero section
    """
    subtitle_html = f"<h2 class='subtitle'>{subtitle}</h2>" if subtitle else ""
    
    # Add background image if provided
    bg_style = ""
    if background_image:
        bg_style = f"background-image: url('{background_image}'); background-size: cover; background-position: center;"
    
    hero_html = f"""
        <div class="hero-section" style="{bg_style}">
            <div class="hero-content">
                <div class="logo">
                    <div class="logo-container">
                        <span class="logo-text">Movie</span>
                        <span class="logo-text-alt">Hub</span>
                    </div>
                </div>
            </div>
            <h1 class="title">{title}</h1>
            {subtitle_html}
        </div>
    """
    
    return hero_html

def info_card(title, content, icon=None):
    """
    Create an information card with a title and content.
    
    Args:
        title (str): Card title
        content (str): Card content
        icon (str, optional): Icon class or emoji
        
    Returns:
        str: HTML for the info card
    """
    icon_html = f"<div class='card-icon'>{icon}</div>" if icon else ""
    
    card_html = f"""
        <div class="card fade-in">
            {icon_html}
            <h3 class="card-title">{title}</h3>
            <div class="card-content">{content}</div>
        </div>
    """
    
    return card_html

def button(text, action=None, button_type="primary"):
    """
    Create a styled button.
    
    Args:
        text (str): Button text
        action (str, optional): URL or action for the button
        button_type (str): Button type (primary or secondary)
        
    Returns:
        str: HTML for the button
    """
    button_html = f"""
        <a href="{action}" class="btn btn-{button_type}">{text}</a>
    """
    
    return button_html

def loading_spinner():
    """
    Create a loading spinner.
    
    Returns:
        str: HTML for the loading spinner
    """
    spinner_html = """
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading...</div>
        </div>
    """
    
    return spinner_html

def tooltip(text, tooltip_text):
    """
    Create a tooltip that appears on hover.
    
    Args:
        text (str): Text to display
        tooltip_text (str): Text to show in tooltip
        
    Returns:
        str: HTML for the tooltip
    """
    tooltip_html = f"""
        <div class="tooltip">
            {text}
            <span class="tooltip-text">{tooltip_text}</span>
        </div>
    """
    
    return tooltip_html

def theme_toggle_button():
    """
    Create a theme toggle button.
    
    Returns:
        str: HTML for the theme toggle button
    """
    toggle_html = """
        <div class="theme-toggle" id="theme-toggle">
            <span class="theme-icon">🌙</span>
        </div>
    """
    
    return toggle_html

def movie_details_section(movie_data):
    """
    Create a detailed movie information section.
    
    Args:
        movie_data (dict): Dictionary containing movie details
        
    Returns:
        str: HTML for the movie details section
    """
    # Extract data from dictionary
    title = movie_data.get('title', 'Unknown Title')
    poster_url = movie_data.get('poster_url', '')
    overview = movie_data.get('overview', 'No overview available.')
    release_date = movie_data.get('release_date', 'Unknown')
    runtime = movie_data.get('runtime', 'Unknown')
    genres = movie_data.get('genres', [])
    rating = movie_data.get('rating', None)
    director = movie_data.get('director', 'Unknown')
    cast = movie_data.get('cast', [])
    
    # Format genres
    genres_html = ""
    if genres:
        genres_html = "<div class='movie-genres-list'>"
        for genre in genres:
            genres_html += f"<span class='genre-tag'>{genre}</span>"
        genres_html += "</div>"
    
    # Format cast
    cast_html = ""
    if cast:
        cast_html = "<div class='movie-cast'>"
        for actor in cast[:5]:  # Show only first 5 cast members
            cast_html += f"<span class='cast-member'>{actor}</span>"
        if len(cast) > 5:
            cast_html += f"<span class='cast-more'>+{len(cast) - 5} more</span>"
        cast_html += "</div>"
    
    # Create the details section HTML
    details_html = f"""
        <div class="movie-details fade-in">
            <div class="movie-details-header">
                <div class="movie-details-poster">
                    <img src="{poster_url}" alt="{title}">
                </div>
                <div class="movie-details-info">
                    <h2 class="movie-details-title">{title}</h2>
                    <div class="movie-details-meta">
                        <span class="movie-details-year">{release_date}</span>
                        <span class="movie-details-runtime">{runtime} min</span>
                        {f"<span class='movie-details-rating'>★ {rating}/10</span>" if rating else ""}
                    </div>
                    {genres_html}
                    <div class="movie-details-director">
                        <span class="director-label">Director:</span> {director}
                    </div>
                    {cast_html}
                </div>
            </div>
            <div class="movie-details-overview">
                <h3>Overview</h3>
                <p>{overview}</p>
            </div>
        </div>
    """
    
    return details_html 