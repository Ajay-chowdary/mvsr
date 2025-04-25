import nltk
import os

def download_nltk_data():
    """
    Download required NLTK data for the movie recommendation system.
    """
    print("Downloading required NLTK data...")
    
    # Create NLTK data directory if it doesn't exist
    nltk_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Set NLTK data path
    nltk.data.path.append(nltk_data_dir)
    
    # Download required NLTK data
    try:
        # Download stopwords
        nltk.download('stopwords', download_dir=nltk_data_dir)
        print("✓ Downloaded stopwords")
        
        # Download punkt tokenizer
        nltk.download('punkt', download_dir=nltk_data_dir)
        print("✓ Downloaded punkt tokenizer")
        
        # Download wordnet for lemmatization
        nltk.download('wordnet', download_dir=nltk_data_dir)
        print("✓ Downloaded wordnet")
        
        # Download averaged perceptron tagger
        nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_dir)
        print("✓ Downloaded averaged perceptron tagger")
        
        print("\nAll required NLTK data has been downloaded successfully!")
        
    except Exception as e:
        print(f"Error downloading NLTK data: {str(e)}")
        print("Please try running this script again or download the data manually.")

if __name__ == "__main__":
    download_nltk_data() 