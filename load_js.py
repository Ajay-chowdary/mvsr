import streamlit as st
import os

def load_js(js_file):
    """
    Load a JavaScript file into the Streamlit app.
    
    Args:
        js_file (str): Path to the JavaScript file
    """
    with open(js_file) as f:
        js_code = f.read()
        st.markdown(f'<script>{js_code}</script>', unsafe_allow_html=True)

def load_js_from_string(js_string):
    """
    Load JavaScript from a string into the Streamlit app.
    
    Args:
        js_string (str): JavaScript as a string
    """
    st.markdown(f'<script>{js_string}</script>', unsafe_allow_html=True)

def apply_custom_js():
    """
    Apply custom JavaScript to the Streamlit app.
    """
    # Check if script.js exists
    if os.path.exists('script.js'):
        load_js('script.js')
    else:
        # Fallback to inline JavaScript if file doesn't exist
        load_js_from_string("""
            // Basic theme toggle functionality
            document.addEventListener('DOMContentLoaded', function() {
                const themeToggle = document.getElementById('theme-toggle');
                if (themeToggle) {
                    themeToggle.addEventListener('click', function() {
                        const currentTheme = document.body.getAttribute('data-theme') || 'dark';
                        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                        
                        document.body.setAttribute('data-theme', newTheme);
                        
                        // Update theme icon
                        const themeIcon = themeToggle.querySelector('.theme-icon');
                        if (themeIcon) {
                            themeIcon.textContent = newTheme === 'dark' ? '🌙' : '☀️';
                        }
                    });
                }
            });
        """) 