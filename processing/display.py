import os
from processing import preprocess
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

class Main():

    def __enter__(self):
        # Initialization code, if needed
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup code, if needed
        pass

    def __init__(self):
        self.new_df = None
        self.movies = None
        self.movies2 = None

    def getter(self):
        return self.new_df, self.movies, self.movies2

    def get_df(self):
        try:
            # Check if Files directory exists
            if not os.path.exists('Files'):
                st.error("Files directory not found. Please run setup.py first.")
                return self
            
            # Check if pickle files exist
            pickle_files = [
                'Files/movies_dict.pkl',
                'Files/movies2_dict.pkl',
                'Files/new_df_dict.pkl'
            ]
            
            missing_files = [f for f in pickle_files if not os.path.exists(f)]
            if missing_files:
                st.warning(f"Missing pickle files: {', '.join(missing_files)}. Regenerating data...")
                self.movies, self.new_df, self.movies2 = preprocess.read_csv_to_df()
                self._save_pickle_files()
                return self
            
            # Try to load pickle files
            try:
                # Load movies dataframe
                with open('Files/movies_dict.pkl', 'rb') as pickle_file:
                    loaded_dict = pickle.load(pickle_file)
                self.movies = pd.DataFrame.from_dict(loaded_dict)
                
                # Load movies2 dataframe
                with open('Files/movies2_dict.pkl', 'rb') as pickle_file:
                    loaded_dict_2 = pickle.load(pickle_file)
                self.movies2 = pd.DataFrame.from_dict(loaded_dict_2)
                
                # Load new_df dataframe
                with open('Files/new_df_dict.pkl', 'rb') as pickle_file:
                    loaded_dict = pickle.load(pickle_file)
                self.new_df = pd.DataFrame.from_dict(loaded_dict)
                
                # Check if similarity files exist
                similarity_files = [
                    'Files/similarity_tags_tags.pkl',
                    'Files/similarity_tags_genres.pkl',
                    'Files/similarity_tags_keywords.pkl',
                    'Files/similarity_tags_tcast.pkl',
                    'Files/similarity_tags_tprduction_comp.pkl'
                ]
                
                missing_similarity = [f for f in similarity_files if not os.path.exists(f)]
                if missing_similarity:
                    st.warning(f"Missing similarity files: {', '.join(missing_similarity)}. Regenerating...")
                    self._generate_similarity_files()
                
            except Exception as e:
                st.error(f"Error loading pickle files: {str(e)}. Regenerating data...")
                self.movies, self.new_df, self.movies2 = preprocess.read_csv_to_df()
                self._save_pickle_files()
                self._generate_similarity_files()
            
            return self
            
        except Exception as e:
            st.error(f"Unexpected error in get_df: {str(e)}")
            return self
    
    def _save_pickle_files(self):
        """Helper method to save pickle files"""
        try:
            # Save movies dataframe
            with open('Files/movies_dict.pkl', 'wb') as f:
                pickle.dump(self.movies.to_dict(), f, protocol=4)
            
            # Save movies2 dataframe
            with open('Files/movies2_dict.pkl', 'wb') as f:
                pickle.dump(self.movies2.to_dict(), f, protocol=4)
            
            # Save new_df dataframe
            with open('Files/new_df_dict.pkl', 'wb') as f:
                pickle.dump(self.new_df.to_dict(), f, protocol=4)
                
            st.success("Pickle files saved successfully!")
        except Exception as e:
            st.error(f"Error saving pickle files: {str(e)}")
    
    def _generate_similarity_files(self):
        """Helper method to generate similarity files"""
        try:
            # Generate similarity matrices for different features
            features = ['tags', 'genres', 'keywords', 'tcast', 'tprduction_comp']
            
            for feature in features:
                similarity = self.vectorise(feature)
                
                # Save similarity matrix
                with open(f'Files/similarity_tags_{feature}.pkl', 'wb') as f:
                    pickle.dump(similarity, f, protocol=4)
            
            st.success("Similarity files generated successfully!")
        except Exception as e:
            st.error(f"Error generating similarity files: {str(e)}")

    def vectorise(self, col_name):
        """Model to vectorise the words using CountVectorizer (Bag of words)"""
        try:
            cv = CountVectorizer(max_features=5000, stop_words='english')
            vec_tags = cv.fit_transform(self.new_df[col_name]).toarray()
            sim_bt = cosine_similarity(vec_tags)
            return sim_bt
        except Exception as e:
            st.error(f"Error in vectorise: {str(e)}")
            return None

    def get_similarity(self, col_name):
        """Get similarity matrix for a specific column"""
        try:
            pickle_file_path = f'Files/similarity_tags_{col_name}.pkl'
            
            if os.path.exists(pickle_file_path):
                with open(pickle_file_path, 'rb') as f:
                    return pickle.load(f)
            else:
                similarity = self.vectorise(col_name)
                if similarity is not None:
                    with open(pickle_file_path, 'wb') as f:
                        pickle.dump(similarity, f, protocol=4)
                return similarity
        except Exception as e:
            st.error(f"Error in get_similarity: {str(e)}")
            return None

    def main_(self):
        # This is to make sure that resources are available.
        self.get_df()
        self.get_similarity('tags')
        self.get_similarity('genres')
        self.get_similarity('keywords')
        self.get_similarity('tcast')
        self.get_similarity('tprduction_comp')
