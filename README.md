# Movie Recommendation System

A content-based movie recommendation system that suggests movies based on various features including genres, cast, crew, and plot keywords.

## Features

- Content-based movie recommendations
- Multiple recommendation criteria (genres, cast, crew, keywords)
- Movie poster display
- Actor information and their movies
- Modern and user-friendly interface

## Prerequisites

- Python 3.7+
- Required Python packages (install using `pip install -r requirements.txt`):
  - streamlit
  - pandas
  - numpy
  - scikit-learn
  - nltk
  - requests
  - Pillow

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd moviesrecomm-main
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Place the required CSV files in the `Files` directory:
   - `tmdb_5000_credits.csv`
   - `tmdb_5000_movies.csv`

4. Run the setup script to initialize the application:
```bash
python setup.py
```

5. Start the Streamlit application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `setup.py`: Setup script for initializing the application
- `processing/`: Directory containing data processing modules
  - `preprocess.py`: Data preprocessing and recommendation logic
- `Files/`: Directory for storing data files and generated pickle files

## Usage

1. Select a movie from the dropdown menu
2. Choose recommendation criteria (genres, cast, crew, keywords)
3. View recommended movies with their posters and details
4. Click on actor names to view their information and movies

## Error Handling

The application includes comprehensive error handling for:
- Missing data files
- API request failures
- Data processing errors
- NLTK resource management

## Contributing

Feel free to submit issues and enhancement requests! 