import os
import nltk
import streamlit as st
from processing.preprocess import read_csv_to_df, vectorise
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
from nltk.stem.porter import PorterStemmer
import string

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ['Files', 'processing/nltk_data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def setup_nltk():
    """Setup NLTK data"""
    try:
        # Create nltk_data directory
        nltk_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'processing', 'nltk_data')
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)

        # Set NLTK data path
        nltk.data.path.append(nltk_data_dir)

        # Download required NLTK data
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords', download_dir=nltk_data_dir)
        print("NLTK setup complete!")
        return True
    except Exception as e:
        print(f"Error in NLTK setup: {str(e)}")
        return False

def check_required_files():
    """Check if required CSV files exist"""
    required_files = [
        'Files/tmdb_5000_credits.csv',
        'Files/tmdb_5000_movies.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"- {file}")
        return False
    return True

def generate_pickle_files():
    """Generate pickle files from CSV data"""
    try:
        # Read and process CSV files
        movies, new_df, movies2 = read_csv_to_df()
        if movies is None or new_df is None or movies2 is None:
            return False

        # Generate similarity matrices
        print("Generating similarity matrices...")
        similarity_tags = vectorise(new_df, 'tags')
        similarity_keywords = vectorise(new_df, 'keywords')
        similarity_cast = vectorise(new_df, 'tcast')
        similarity_crew = vectorise(new_df, 'tcrew')
        similarity_production = vectorise(new_df, 'tprduction_comp')

        if any(x is None for x in [similarity_tags, similarity_keywords, similarity_cast, 
                                 similarity_crew, similarity_production]):
            return False

        # Save pickle files
        print("Saving pickle files...")
        pickle_files = {
            'Files/movies_dict.pkl': movies.to_dict(),
            'Files/movies2_dict.pkl': movies2.to_dict(),
            'Files/similarity_tags.pkl': similarity_tags,
            'Files/similarity_keywords.pkl': similarity_keywords,
            'Files/similarity_cast.pkl': similarity_cast,
            'Files/similarity_crew.pkl': similarity_crew,
            'Files/similarity_production.pkl': similarity_production
        }

        for file_path, data in pickle_files.items():
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            print(f"Saved: {file_path}")

        return True
    except Exception as e:
        print(f"Error generating pickle files: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("Starting setup...")
    
    # Create directories
    setup_directories()
    
    # Setup NLTK
    if not setup_nltk():
        print("Failed to setup NLTK")
        return False
    
    # Check required files
    if not check_required_files():
        print("Please ensure all required files are present in the Files directory")
        return False
    
    # Generate pickle files
    if not generate_pickle_files():
        print("Failed to generate pickle files")
        return False
    
    print("Setup completed successfully!")
    return True

if __name__ == "__main__":
    main() 