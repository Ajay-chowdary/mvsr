import string
import pickle
import pandas as pd
import ast
import requests
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Create nltk_data directory in the project folder if it doesn't exist
nltk_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

# Set NLTK data path to our custom directory
nltk.data.path.append(nltk_data_dir)

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Object for porterStemmer
ps = PorterStemmer()

def get_genres(obj):
    try:
        lista = ast.literal_eval(obj)
        return [i['name'] for i in lista]
    except:
        return []

def get_cast(obj):
    try:
        a = ast.literal_eval(obj)
        return [a[i]['name'] for i in range(min(10, len(a)))]
    except:
        return []

def get_crew(obj):
    try:
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                return [i['name']]
        return []
    except:
        return []

def read_csv_to_df():
    try:
        # Check if Files directory exists
        if not os.path.exists('Files'):
            st.error("Files directory not found. Please run setup.py first.")
            return None, None, None
            
        # Check if CSV files exist
        if not os.path.exists('Files/tmdb_5000_credits.csv') or not os.path.exists('Files/tmdb_5000_movies.csv'):
            st.error("CSV files not found. Please make sure tmdb_5000_credits.csv and tmdb_5000_movies.csv are in the Files directory.")
            return None, None, None
            
        # Reading both the csv files
        credit_ = pd.read_csv(r'Files/tmdb_5000_credits.csv')
        movies = pd.read_csv(r'Files/tmdb_5000_movies.csv')

        # Merging the dataframes
        movies = movies.merge(credit_, on='title')

        movies2 = movies
        movies2.drop(['homepage', 'tagline'], axis=1, inplace=True)
        movies2 = movies2[['movie_id', 'title', 'budget', 'overview', 'popularity', 'release_date', 'revenue', 'runtime',
                           'spoken_languages', 'status', 'vote_average', 'vote_count']]

        # Extracting important and relevant features
        movies = movies[
            ['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew', 'production_companies', 'release_date']]
        movies.dropna(inplace=True)

        # Applying functions to convert from list to only items.
        movies['genres'] = movies['genres'].apply(get_genres)
        movies['keywords'] = movies['keywords'].apply(get_genres)
        movies['top_cast'] = movies['cast'].apply(get_cast)
        movies['director'] = movies['crew'].apply(get_crew)
        movies['prduction_comp'] = movies['production_companies'].apply(get_genres)

        # Removing spaces from between the lines
        movies['overview'] = movies['overview'].apply(lambda x: x.split())
        movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
        movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
        movies['tcast'] = movies['top_cast'].apply(lambda x: [i.replace(" ", "") for i in x])
        movies['tcrew'] = movies['director'].apply(lambda x: [i.replace(" ", "") for i in x])
        movies['tprduction_comp'] = movies['prduction_comp'].apply(lambda x: [i.replace(" ", "") for i in x])

        # Creating a tags where we have all the words together for analysis
        movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['tcast'] + movies['tcrew']

        # Creating new dataframe for the analysis part only.
        new_df = movies[['movie_id', 'title', 'tags', 'genres', 'keywords', 'tcast', 'tcrew', 'tprduction_comp']]

        new_df['genres'] = new_df['genres'].apply(lambda x: " ".join(x))
        new_df['tcast'] = new_df['tcast'].apply(lambda x: " ".join(x))
        new_df['tprduction_comp'] = new_df['tprduction_comp'].apply(lambda x: " ".join(x))

        new_df['tcast'] = new_df['tcast'].apply(lambda x: x.lower())
        new_df['genres'] = new_df['genres'].apply(lambda x: x.lower())
        new_df['tprduction_comp'] = new_df['tprduction_comp'].apply(lambda x: x.lower())

        # Applying stemming on tags and tags and keywords
        new_df['tags'] = new_df['tags'].apply(stemming_stopwords)
        new_df['keywords'] = new_df['keywords'].apply(stemming_stopwords)

        return movies, new_df, movies2
    except Exception as e:
        st.error(f"Error in read_csv_to_df: {str(e)}")
        return None, None, None

def stemming_stopwords(li):
    try:
        # Initialize Porter Stemmer
        ps = PorterStemmer()
        ans = []

        # Apply stemming
        for i in li:
            ans.append(ps.stem(i))

        try:
            # Try to get stopwords
            stop_words = set(stopwords.words('english'))
        except LookupError:
            # If stopwords aren't available, use a basic set of common English stopwords
            stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
                         "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
                         'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 
                         'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
                         'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 
                         'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
                         'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
                         'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
                         'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 
                         'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
                         'then', 'once'}

        # Remove stopwords and create filtered sentence
        filtered_sentence = []
        for w in ans:
            w = w.lower()
            if w not in stop_words:
                filtered_sentence.append(w)

        # Join words with spaces
        str_ = ' '.join(word for word in filtered_sentence if len(word) > 2)

        # Remove punctuation
        str_ = ''.join(char for char in str_ if char not in string.punctuation)
        return str_
    except Exception as e:
        # If any error occurs, return an empty string
        print(f"Error in stemming_stopwords: {str(e)}")
        return ''

def fetch_posters(movie_id):
    try:
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=076aa064daba31efd326e9d7e5444c2d'.format(movie_id))
        data = response.json()
        try:
            str_ = "https://image.tmdb.org/t/p/w780/" + data['poster_path']
        except:
            str_ = "https://media.istockphoto.com/vectors/error-icon-vector-illustration-vector-id922024224?k=6&m" \
                   "=922024224&s=612x612&w=0&h=LXl8Ul7bria6auAXKIjlvb6hRHkAodTqyqBeA6K7R54="

        return str_
    except Exception as e:
        print(f"Error in fetch_posters: {str(e)}")
        return "https://media.istockphoto.com/vectors/error-icon-vector-illustration-vector-id922024224?k=6&m" \
               "=922024224&s=612x612&w=0&h=LXl8Ul7bria6auAXKIjlvb6hRHkAodTqyqBeA6K7R54="

def recommend(new_df, movie, pickle_file_path):
    try:
        with open(pickle_file_path, 'rb') as pickle_file:
            similarity_tags = pickle.load(pickle_file)

        movie_idx = new_df[new_df['title'] == movie].index[0]

        # Getting the top 25 movies from the list which are most similar
        movie_list = sorted(list(enumerate(similarity_tags[movie_idx])), reverse=True, key=lambda x: x[1])[1:26]

        rec_movie_list = []
        rec_poster_list = []

        for i in movie_list:
            rec_movie_list.append(new_df.iloc[i[0]]['title'])
            rec_poster_list.append(fetch_posters(new_df.iloc[i[0]]['movie_id']))

        return rec_movie_list, rec_poster_list
    except Exception as e:
        st.error(f"Error in recommend: {str(e)}")
        return [], []

def vectorise(new_df, col_name):
    try:
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vec_tags = cv.fit_transform(new_df[col_name]).toarray()
        sim_bt = cosine_similarity(vec_tags)
        return sim_bt
    except Exception as e:
        st.error(f"Error in vectorise: {str(e)}")
        return None

def fetch_person_details(id_):
    try:
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
    except Exception as e:
        print(f"Error in fetch_person_details: {str(e)}")
        return "https://media.istockphoto.com/vectors/error-icon-vector-illustration-vector-id922024224?k=6&m" \
               "=922024224&s=612x612&w=0&h=LXl8Ul7bria6auAXKIjlvb6hRHkAodTqyqBeA6K7R54=", ""

def get_details(selected_movie_name):
    try:
        # Loading both the dataframes for fast reading
        pickle_file_path = r'Files/movies_dict.pkl'
        with open(pickle_file_path, 'rb') as pickle_file:
            loaded_dict = pickle.load(pickle_file)

        movies = pd.DataFrame.from_dict(loaded_dict)

        pickle_file_path = r'Files/movies2_dict.pkl'
        with open(pickle_file_path, 'rb') as pickle_file:
            loaded_dict_2 = pickle.load(pickle_file)

        movies2 = pd.DataFrame.from_dict(loaded_dict_2)

        # Extracting series of data to be displayed
        a = pd.DataFrame(movies2[movies2['title'] == selected_movie_name])
        b = pd.DataFrame(movies[movies['title'] == selected_movie_name])

        if a.empty or b.empty:
            st.warning(f"No details found for movie: {selected_movie_name}")
            return None

        # Extracting necessary details
        budget = a.iloc[0, 2]
        overview = a.iloc[0, 3]
        release_date = a.iloc[:, 5].iloc[0]
        revenue = a.iloc[:, 6].iloc[0]
        runtime = a.iloc[:, 7].iloc[0]
        available_lang = ast.literal_eval(a.iloc[0, 8])
        vote_rating = a.iloc[:, 10].iloc[0]
        vote_count = a.iloc[:, 11].iloc[0]
        movie_id = a.iloc[:, 0].iloc[0]
        cast = b.iloc[:, 9].iloc[0]
        director = b.iloc[:, 10].iloc[0]
        genres = b.iloc[:, 3].iloc[0]
        this_poster = fetch_posters(movie_id)
        cast_per = b.iloc[:, 5].iloc[0]
        a = ast.literal_eval(cast_per)
        cast_id = []
        for i in a:
            cast_id.append(i['id'])
        lang = []
        for i in available_lang:
            lang.append(i['name'])

        # Adding to a list for easy export
        info = [this_poster, budget, genres, overview, release_date, revenue, runtime, available_lang, vote_rating,
                vote_count, movie_id, cast, director, lang, cast_id]

        return info
    except Exception as e:
        st.error(f"Error in get_details: {str(e)}")
        return None

def fetch_cast_images(cast_ids):
    """Fetch cast member profile images from TMDB API"""
    try:
        cast_images = []
        for cast_id in cast_ids[:5]:  # Limit to first 5 cast members
            try:
                response = requests.get(
                    f'https://api.themoviedb.org/3/person/{cast_id}?api_key=076aa064daba31efd326e9d7e5444c2d'
                )
                data = response.json()
                if data.get('profile_path'):
                    image_url = f"https://image.tmdb.org/t/p/w185{data['profile_path']}"
                else:
                    image_url = "https://via.placeholder.com/185x278?text=No+Image"
                cast_images.append(image_url)
            except:
                cast_images.append("https://via.placeholder.com/185x278?text=No+Image")
        return cast_images
    except Exception as e:
        print(f"Error in fetch_cast_images: {str(e)}")
        return ["https://via.placeholder.com/185x278?text=No+Image"] * 5

def fetch_actor_movies(actor_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key=076aa064daba31efd326e9d7e5444c2d'
        )
        data = response.json()
        movies = []
        posters = []
        
        for movie in data.get('cast', [])[:8]:  # Limit to 8 movies
            if movie.get('poster_path'):
                movies.append(movie['title'])
                poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                posters.append(poster_url)
                
        return movies, posters
    except Exception as e:
        print(f"Error in fetch_actor_movies: {str(e)}")
        return [], []




