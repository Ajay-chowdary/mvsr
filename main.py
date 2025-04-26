import streamlit as st
import base64
from pathlib import Path
import os
print(os.path.exists('image.jpg'))  # Should return True


# Must be the first Streamlit command
st.set_page_config(
    page_title="Movie Hub",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from processing import preprocess
from processing import display
import pandas as pd
import requests
import ast
import time
import pickle

# TMDB API key
TMDB_API_KEY = "076aa064daba31efd326e9d7e5444c2d"

# Initialize session state for actor movies
if 'show_actor_movies' not in st.session_state:
    st.session_state.show_actor_movies = None

def fetch_posters(movie_id):
    """
    Fetch the poster URL for a given movie ID using TMDB API.
    """
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    )
    data = response.json()
    try:
        return f"https://image.tmdb.org/t/p/w780/{data['poster_path']}"
    except KeyError:
        return "https://via.placeholder.com/150"

def recommend_display(new_df):
    """
    Display movie recommendations and handle movie selection with a predictive dropdown.
    """
    st.markdown("<h1 class='title'>🎥 Movie Hub</h1>", unsafe_allow_html=True)
    
    # Get all movie titles that have complete details
    valid_movies = []
    for movie in new_df["title"].dropna().unique():
        if preprocess.get_details(movie) is not None:
            valid_movies.append(movie)
    
    # Create searchable dropdown with only valid movies
    search_query = st.selectbox(
        "Search for a Movie:",
        options=[""] + sorted(valid_movies),
        format_func=lambda x: "🔍 Type to search..." if x == "" else f"🎬 {x}",
        key="movie_search"
    )

    if st.button('Show Details', type="primary", use_container_width=True):
        if search_query and search_query != "🔍 Type to search...":
            st.session_state.selected_movie_name = search_query
            st.rerun()

def display_movie_details_and_recommendations(new_df):
    # Add this CSS at the start of the function
    st.markdown("""
        <style>
        /* Hide Streamlit's fullscreen button */
        button[title="View fullscreen"] {
            display: none !important;
        }
        
        /* Remove pointer cursor from images */
        .stImage > img {
            cursor: default !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    selected_movie_name = st.session_state.get("selected_movie_name", None)
    
    if selected_movie_name:
        try:
            movie_details = preprocess.get_details(selected_movie_name)
            
            if movie_details is None:
                st.warning("Please select another movie. Complete details not available for this selection.")
                return
            
            if movie_details:
                # Main movie details section
                col_poster, col_info = st.columns([1, 2], gap="large")
                
                with col_poster:
                    st.markdown(f'''
                        <div style="position: relative;">
                            <img src="{movie_details[0]}" 
                                 style="width: 100%; 
                                        border-radius: 10px; 
                                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                                        pointer-events: none;">
                            <div style="position: absolute; 
                                      top: 10px; 
                                      right: 10px; 
                                      background: rgba(0,0,0,0.7); 
                                      padding: 5px 10px; 
                                      border-radius: 20px; 
                                      color: gold;">
                                ★ {movie_details[8]}/10
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                with col_info:
                    st.markdown(f"""
                        <div style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem; color: white;">
                            {selected_movie_name}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # First, add Material Design Icons CDN at the start of your function
                    st.markdown("""
                        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@7.2.96/css/materialdesignicons.min.css" rel="stylesheet">
                        <style>
                            .mdi {
                                font-size: 1.4rem;
                                vertical-align: middle;
                            }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    # Then replace the metadata section with this enhanced version
                    st.markdown(f"""
                        <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
                            <span style="background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%); 
                                        padding: 0.7rem 1.2rem; 
                                        border-radius: 20px; 
                                        display: flex; 
                                        align-items: center; 
                                        gap: 0.7rem;
                                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <i class="mdi mdi-calendar-star" style="color: #82b1ff;"></i>
                                {movie_details[4]}
                            </span>
                            <span style="background: linear-gradient(135deg, #311b92 0%, #4527a0 100%); 
                                        padding: 0.7rem 1.2rem; 
                                        border-radius: 20px; 
                                        display: flex; 
                                        align-items: center; 
                                        gap: 0.7rem;
                                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <i class="mdi mdi-timer-outline" style="color: #b388ff;"></i>
                                {movie_details[6]} min
                            </span>
                            <span style="background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%); 
                                        padding: 0.7rem 1.2rem; 
                                        border-radius: 20px; 
                                        display: flex; 
                                        align-items: center; 
                                        gap: 0.7rem;
                                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <i class="mdi mdi-currency-usd" style="color: #69f0ae;"></i>
                                ${"{:,.0f}".format(float(movie_details[1]))}
                            </span>
                            <span style="background: linear-gradient(135deg, #bf360c 0%, #d84315 100%); 
                                        padding: 0.7rem 1.2rem; 
                                        border-radius: 20px; 
                                        display: flex; 
                                        align-items: center; 
                                        gap: 0.7rem;
                                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                <i class="mdi mdi-star-face" style="color: #ffab91;"></i>
                                {movie_details[8]}/10
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                        <div style="font-size: 1.5rem; font-weight: bold; margin: 1.5rem 0 1rem 0; color: white;">
                            Overview
                        </div>
                    """, unsafe_allow_html=True)
                    st.write(movie_details[3])
                
                # Cast section with custom styling
                st.markdown("""
                    <div style="font-size: 1.5rem; 
                                font-weight: bold; 
                                margin: 2.5rem 0 1.5rem 0; 
                                color: white !important;
                                text-align: center;
                                pointer-events: none;">
                        Featured Cast
                    </div>
                """, unsafe_allow_html=True)

                # Initialize session state for actor movies if not exists
                if 'show_actor_movies' not in st.session_state:
                    st.session_state.show_actor_movies = None

                cast_cols = st.columns(4)
                for idx, (cast_id, cast_name) in enumerate(zip(movie_details[14][:4], movie_details[11][:4])):
                    with cast_cols[idx]:
                        url, bio = fetch_person_details(cast_id)
                        st.markdown(f'''
                            <div style="text-align: center; 
                                        padding: 1rem;
                                        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
                                        border-radius: 12px;
                                        border: 1px solid rgba(255,255,255,0.1);
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                                        pointer-events: none;">
                                <img src="{url}" 
                                     style="width: 140px; 
                                            height: 180px; 
                                            object-fit: cover; 
                                            border-radius: 10px; 
                                            margin-bottom: 1rem;
                                            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                                            pointer-events: none;">
                                <p style="margin: 0; 
                                          font-weight: 600; 
                                          color: white !important;
                                          font-size: 1.1rem;
                                          pointer-events: none;">
                                    {cast_name}
                                </p>
                            </div>
                        ''', unsafe_allow_html=True)
                        
                        if st.button("View Movies", key=f"cast_{idx}", use_container_width=True, type="primary"):
                            st.session_state.show_actor_movies = (cast_id, cast_name, url)
                            st.rerun()

                # Display actor movies if selected
                if st.session_state.show_actor_movies:
                    cast_id, cast_name, cast_url = st.session_state.show_actor_movies
                    
                    # Fetch actor's movies BEFORE creating the layout
                    actor_movies, actor_posters = preprocess.fetch_actor_movies(cast_id)
                    
                    # Only proceed with display if we have movies
                    if actor_movies and actor_posters:
                        st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.75) 100%);
                                padding: 2rem;
                                border-radius: 20px;
                                margin: 3rem 0;
                                backdrop-filter: blur(10px);
                                border: 1px solid rgba(255,255,255,0.1);">
                                <div style="
                                    display: flex;
                                    align-items: center;
                                    gap: 2rem;
                                    margin-bottom: 2rem;
                                    padding: 1.5rem;
                                    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                                    border-radius: 15px;
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                                    <img src="{cast_url}" 
                                         style="width: 80px;
                                                height: 80px;
                                                object-fit: cover;
                                                border-radius: 50%;
                                                border: 3px solid rgba(255,255,255,0.2);
                                                pointer-events: none;">
                                    <div style="margin: 0; 
                                              color: white;
                                              font-size: 1.5rem;
                                              font-weight: 600;
                                              pointer-events: none;">
                                        Movies featuring {cast_name}
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        # Create grid layout for movies
                        cols = st.columns(4)
                        for m_idx, (movie, poster) in enumerate(zip(actor_movies, actor_posters)):
                            with cols[m_idx % 4]:
                                # First check if movie exists in database
                                movie_exists = False
                                exact_title = None
                                
                                # Try exact match first
                                if movie in new_df['title'].values:
                                    movie_exists = True
                                    exact_title = movie
                                else:
                                    # Try fuzzy matching
                                    for db_title in new_df['title'].values:
                                        # Remove special characters and convert to lowercase for comparison
                                        clean_movie = ''.join(e.lower() for e in movie if e.isalnum())
                                        clean_db_title = ''.join(e.lower() for e in db_title if e.isalnum())
                                        
                                        # Check for exact match after cleaning
                                        if clean_movie == clean_db_title:
                                            movie_exists = True
                                            exact_title = db_title
                                            break
                                        # Check for contained match (for movies with different versions/years)
                                        elif (clean_movie in clean_db_title or clean_db_title in clean_movie) and \
                                             len(clean_movie) > 5:  # Avoid matching very short titles
                                            movie_exists = True
                                            exact_title = db_title
                                            break
                                
                                # Display movie card
                                st.markdown(f'''
                                    <div style="background: rgba(255,255,255,0.05); 
                                            padding: 1.2rem; 
                                            border-radius: 15px; 
                                            margin-bottom: 2rem;
                                            border: 1px solid rgba(255,255,255,0.1);
                                            height: 100%;
                                            box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                                        <img src="{poster}" 
                                             style="width: 100%; 
                                                    height: 300px;
                                                    object-fit: cover;
                                                    border-radius: 12px; 
                                                    margin-bottom: 1rem;
                                                    box-shadow: 0 6px 12px rgba(0,0,0,0.3);">
                                        <div style="margin: 1rem 0; 
                                                  color: white;
                                                  font-size: 1.2rem;
                                                  font-weight: 600;
                                                  text-align: center;
                                                  pointer-events: none;">
                                            {movie}
                                        </div>
                                    </div>
                                ''', unsafe_allow_html=True)
                                
                                if movie_exists and exact_title:
                                    if st.button("View Movie", 
                                               key=f"actor_movie_{m_idx}", 
                                               use_container_width=True,
                                               type="primary"):
                                        st.session_state.selected_movie_name = exact_title
                                        st.session_state.show_actor_movies = None  # Clear the actor movies view
                                        st.rerun()
                
                # Recommendations section
                st.markdown("""
                    <div style="font-size: 2rem; font-weight: bold; text-align: center; margin: 3rem 0 2rem 0; color: white;">
                        You May Also Like
                    </div>
                """, unsafe_allow_html=True)

                recommended_movies, posters = preprocess.recommend(
                    new_df, selected_movie_name, r"Files/similarity_tags_tags.pkl"
                )

                # Display recommendations in a grid
                cols = st.columns(5)
                for idx, (movie, poster) in enumerate(zip(recommended_movies[:20], posters[:20])):
                    with cols[idx % 5]:
                        rec_details = preprocess.get_details(movie)
                        st.markdown(f'''
                            <div style="background: rgba(255,255,255,0.05); 
                                        padding: 1rem; 
                                        border-radius: 10px; 
                                        margin-bottom: 1rem;
                                        border: 1px solid rgba(255,255,255,0.1);
                                        height: 100%;">
                                <img src="{poster}" 
                                     style="width: 100%; 
                                            border-radius: 8px; 
                                            margin-bottom: 0.5rem;
                                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                                <div style="margin: 0.5rem 0; 
                                          color: white;
                                          font-size: 1.1rem;
                                          font-weight: 600;
                                          pointer-events: none;">
                                    {movie}
                                </div>
                                <div style="display: flex; 
                                            justify-content: space-between; 
                                            align-items: center;
                                            margin: 0.5rem 0;
                                            padding-top: 0.5rem;
                                            border-top: 1px solid rgba(255,255,255,0.1);">
                                    <span style="color: gold; 
                                               font-weight: 600;
                                               display: flex;
                                               align-items: center;
                                               gap: 0.3rem;">
                                        <i class="mdi mdi-star"></i>
                                        {rec_details[8]}/10
                                    </span>
                                    <span style="color: rgba(255,255,255,0.6);
                                               font-size: 0.9rem;">
                                        {rec_details[4]}
                                    </span>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)
                        
                        if st.button("View Details", key=f"movie_button_{idx}", 
                                    use_container_width=True,
                                    type="primary"):
                            st.session_state.selected_movie_name = movie
                            st.session_state.recommendation_source = movie
                            st.rerun()
                            
        except Exception as e:
            st.error(f"Error loading movie details: {str(e)}")

def fetch_person_details(id_):
    data = requests.get(
        'https://api.themoviedb.org/3/person/{}?api_key=076aa064daba31efd326e9d7e5444c2d'.format(id_)).json()

    try:
        url = 'https://image.tmdb.org/t/p/w220_and_h330_face' + data['profile_path']

        if data['biography']:
            biography = data['biography']
        else:
            biography = " "

    except:
        url = "https://media.istockphoto.com/vectors/error-icon-vector-illustration-vector-id922024224?k=6&m" \
              "=922024224&s=612x612&w=0&h=LXl8Ul7bria6auAXKIjlvb6hRHkAodTqyqBeA6K7R54="
        biography = ""

    return url, biography

def create_hero_section(new_df):
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, 
                rgba(13, 17, 23, 0.95) 0%, 
                rgba(42, 25, 66, 0.95) 50%,
                rgba(255, 65, 108, 0.3) 100%);
            background-size: 200% 200%;
            animation: gradientBG 15s ease infinite;
            padding: 3rem 2rem;
            border-radius: 24px;
            margin: -6rem -4rem 4rem -4rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle at 50% 50%, 
                    rgba(255, 65, 108, 0.1) 0%,
                    transparent 50%);
                animation: pulse 4s ease-in-out infinite;
            "></div>
            <div style="
                position: relative;
                z-index: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 2rem;
                margin-bottom: 3rem;
            ">
                <div class="logo" style="
                    font-family: 'Montserrat', sans-serif;
                    margin-bottom: 1.5rem;
                ">
                    <div style="
                        display: inline-flex;
                        align-items: center;
                        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
                        padding: 0.8rem 1.5rem;
                        border-radius: 15px;
                        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
                        transform: rotate(-2deg);
                        animation: float 6s ease-in-out infinite;
                    ">
                        <span style="
                            font-size: 3.5rem;
                            font-weight: 800;
                            background: linear-gradient(to right, #fff, #e0e0e0);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            margin-right: 0.5rem;
                        ">Movie</span>
                        <span style="
                            font-size: 3.5rem;
                            font-weight: 800;
                            color: #fff;
                            position: relative;
                        ">Hub
                            <svg width="30" height="30" viewBox="0 0 24 24" style="
                                position: absolute;
                                top: -10px;
                                right: -20px;
                                fill: #FFD700;
                                animation: spin 4s linear infinite;
                            ">
                                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                            </svg>
                        </span>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');
            
            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            @keyframes pulse {
                0% { transform: scale(1); opacity: 0.5; }
                50% { transform: scale(1.5); opacity: 0.2; }
                100% { transform: scale(1); opacity: 0.5; }
            }
            
            @keyframes float {
                0% { transform: rotate(-2deg) translateY(0px); }
                50% { transform: rotate(-2deg) translateY(-10px); }
                100% { transform: rotate(-2deg) translateY(0px); }
            }
            
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)

    # Add Streamlit search component in a container
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            # Get all movie titles
            movie_titles = sorted(new_df["title"].dropna().unique())
            
            # Create searchable dropdown
            selected_movie = st.selectbox(
                "🔍 Search for movies...",
                options=[""] + movie_titles,
                key="movie_search",
                format_func=lambda x: "Type to search..." if x == "" else x
            )

            if selected_movie and selected_movie != "Type to search...":
                if st.button('Show Details', 
                           type="primary", 
                           use_container_width=True,
                           key='search_button'):
                    st.session_state.selected_movie_name = selected_movie
                    st.rerun()

    # Add custom CSS for the search box
    st.markdown("""
        <style>
        /* Search box styling */
        .stSelectbox > div > div {
            background-color: rgba(255, 255, 255, 0.15) !important;
            border: 2px solid #FF416C !important;
            border-radius: 12px !important;
            color: #FFFFFF !important;
            padding: 1rem 1.2rem !important;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.2) !important;
            font-family: 'Montserrat', sans-serif !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
        }

        /* Dropdown styling */
        div[data-baseweb="popover"] {
            background-color: rgba(15, 23, 42, 0.98) !important;
            border: 1px solid #FF416C !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(255, 65, 108, 0.3) !important;
        }

        /* Dropdown options styling */
        div[data-baseweb="select"] ul[role="listbox"] li {
            color: #FFFFFF !important;
            padding: 1rem 1.2rem !important;
            border-bottom: 1px solid rgba(255, 65, 108, 0.2) !important;
            background-color: rgba(15, 23, 42, 0.98) !important;
            transition: all 0.3s ease !important;
            font-family: 'Montserrat', sans-serif !important;
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.5px !important;
        }

        div[data-baseweb="select"] ul[role="listbox"] li:hover {
            background-color: rgba(255, 65, 108, 0.2) !important;
            color: #FF416C !important;
            font-weight: 700 !important;
            transform: translateX(5px) !important;
        }

        /* Selected option in dropdown */
        div[data-baseweb="select"] ul[role="listbox"] li[aria-selected="true"] {
            background-color: rgba(255, 65, 108, 0.25) !important;
            color: #FF416C !important;
            font-weight: 700 !important;
        }

        /* Selected text in search box */
        div[data-baseweb="select"] > div > div {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }

        /* Selected value text */
        div[data-baseweb="select"] > div > div > div {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }

        /* Dropdown text styling */
        div[data-baseweb="select"] span {
            color: #FFFFFF !important;
            font-weight: 500 !important;
            font-family: 'Montserrat', sans-serif !important;
        }

        /* Label styling */
        .stSelectbox label {
            color: #FFFFFF !important;
            font-size: 1.4rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.8rem !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
            font-family: 'Montserrat', sans-serif !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
        }

        /* Placeholder text styling */
        div[data-baseweb="select"] div[data-testid="stMarkdown"] {
            color: rgba(255, 255, 255, 0.7) !important;
            font-weight: 500 !important;
            font-family: 'Montserrat', sans-serif !important;
            font-size: 1.2rem !important;
            letter-spacing: 0.5px !important;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.8rem 1.5rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3) !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(255, 65, 108, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_file):
    # Set a clean gradient background
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
        </style>
    """, unsafe_allow_html=True)

def set_custom_styles():
    st.markdown("""
        <style>
            /* Remove all hover effects and cursors */
            * {
                pointer-events: auto !important;
                cursor: default !important;
                text-decoration: none !important;
            }
            
            /* Remove link styling and hover effects */
            a, a:hover, a:visited, a:active, a:link {
                text-decoration: none !important;
                cursor: default !important;
                pointer-events: none !important;
                color: inherit !important;
            }
            
            /* Remove hover styling from images */
            img {
                pointer-events: none !important;
                user-select: none !important;
                -webkit-user-drag: none !important;
            }
            
            /* Keep buttons and inputs functional */
            .stButton button,
            .stSelectbox > div > div,
            div[data-baseweb="select"] ul li,
            input,
            select {
                cursor: pointer !important;
                pointer-events: auto !important;
            }
            
            /* Remove link decorations from all elements */
            [data-testid="stMarkdown"] a {
                text-decoration: none !important;
                pointer-events: none !important;
            }
            
            /* Remove hover effects from cards */
            .element-container:hover {
                transform: none !important;
            }
            
            /* Disable text selection */
            .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
                user-select: none !important;
            }
            
            /* Keep existing color scheme */
            .stApp, .stMarkdown, p, span {
                color: rgba(255, 255, 255, 0.9) !important;
            }
            
            /* Rest of your existing styles... */
        </style>
    """, unsafe_allow_html=True)

def create_theme_toggle():
    # Create a container in the sidebar for the theme toggle
    with st.sidebar:
        st.markdown("""
            <style>
            /* Theme toggle container styling */
            .stRadio > label {
                color: white !important;
                font-size: 1.1rem !important;
                font-weight: 500 !important;
                margin-bottom: 1rem !important;
            }
            
            /* Radio button options styling */
            .stRadio > div {
                background-color: rgba(255, 255, 255, 0.1) !important;
                padding: 1rem !important;
                border-radius: 12px !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }
            
            /* Radio button label styling */
            .stRadio label {
                color: white !important;
                font-size: 1rem !important;
                font-weight: 500 !important;
            }
            
            /* Selected radio button styling */
            .stRadio [data-baseweb="radio"] {
                background-color: rgba(255, 255, 255, 0.2) !important;
                border-color: white !important;
            }
            
            /* Radio button text styling */
            .stRadio span {
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        theme = st.radio(
            "Choose Theme",
            ["Dark", "Light"],
            key="theme_toggle"
        )
        
        if theme == "Light":
            st.markdown("""
                <style>
                    .stApp {
                        background-color: white !important;
                    }
                    
                    .stApp * {
                        color: #1a1a1a !important;
                    }
                    
                    .stButton button {
                        background-color: #2196F3 !important;
                        color: white !important;
                    }
                    
                    div[style*="background: rgba(255,255,255,0.05)"] {
                        background: rgba(0, 0, 0, 0.05) !important;
                        border: 1px solid rgba(0, 0, 0, 0.1) !important;
                    }
                </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <style>
                    .stApp {
                        background-color: #0e1117 !important;
                    }
                    
                    .stApp * {
                        color: rgba(255, 255, 255, 0.9) !important;
                    }
                </style>
            """, unsafe_allow_html=True)

def set_theme_config():
    """
    Configure the theme settings for the Streamlit app.
    """
    st.markdown("""
        <style>
        /* Main content area */
       
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            background: transparent;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        
        /* Adjust header padding */
        .stApp header {
            background: transparent;
        }
        
        /* Style for all buttons */
        .stButton button {
            background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
        }
        
        /* Title styling */
        .title {
            text-align: center;
            color: white;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    set_background('image.jpg')
    set_custom_styles()
    set_theme_config()
    display_obj = display.Main()
    display_obj.get_df()
    new_df = display_obj.new_df
    
    # Create the hero section with search
    create_hero_section(new_df)
    
    # Display movie details if a movie is selected
    if "selected_movie_name" in st.session_state and st.session_state.selected_movie_name:
        display_movie_details_and_recommendations(new_df)

if __name__ == "__main__":
    main()
