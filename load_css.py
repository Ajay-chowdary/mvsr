import streamlit as st
import os

def load_css(css_file):
    """
    Load a CSS file into the Streamlit app.
    
    Args:
        css_file (str): Path to the CSS file
    """
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_css_from_string(css_string):
    """
    Load CSS from a string into the Streamlit app.
    
    Args:
        css_string (str): CSS as a string
    """
    st.markdown(f'<style>{css_string}</style>', unsafe_allow_html=True)

def apply_custom_styles():
    """
    Apply custom styles to the Streamlit app.
    """
    # Check if style.css exists
    if os.path.exists('style.css'):
        load_css('style.css')
    else:
        # Fallback to inline styles if file doesn't exist
        load_css_from_string("""
            /* Basic fallback styles */
            .stApp {
                font-family: 'Montserrat', sans-serif;
            }
            
            .title {
                font-size: 2.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #FF416C, #FF4B2B);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
            }
        """) 