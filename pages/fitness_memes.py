import streamlit as st
from auth import init_session_state, check_authenticated
import streamlit as st
from config import apply_dark_theme
import datetime
import os
from PIL import Image
import io
import webbrowser
import urllib.parse
import base64
import requests
from urllib.parse import urlparse

# Constants for image sizing
MAX_IMAGE_WIDTH = 600  # Maximum width for displayed images
MAX_IMAGE_HEIGHT = 600  # Maximum height for displayed images

# Initialize session state for likes, comments and user memes
if 'likes' not in st.session_state:
    st.session_state.likes = {}
if 'comments' not in st.session_state:
    st.session_state.comments = {}
if 'user_memes' not in st.session_state:
    st.session_state.user_memes = []

# Meme database with categories
MEME_DATABASE = {
    "motivation": [
        {
            "title": "Me looking at the gym equipment after saying 'I'll start tomorrow' 100 times 👀",
            "image_url": "https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg",
            "likes": 0,
            "comments":0
        },
        {
            "title": "My muscles after one push-up: Am I a joke to you? 💪",
            "image_url": "https://images.pexels.com/photos/1954524/pexels-photo-1954524.jpeg",
            "likes": 0,
            "comments":0
        }
    ],
    "nutrition": [
        {
            "title": "My protein shake watching me eat an entire pizza 🍕",
            "image_url": "https://images.pexels.com/photos/1547248/pexels-photo-1547248.jpeg",
            "likes": 0,
            "comments":0
        },
        {
            "title": "When someone asks if I'm counting calories while eating my third donut 🍩",
            "image_url": "https://images.pexels.com/photos/1229356/pexels-photo-1229356.jpeg",
            "likes":0,
            "comments":0
        }
    ],
    "workout": [
        {
            "title": "That moment when your pre-workout kicks in ⚡",
            "image_url": "https://images.pexels.com/photos/863988/pexels-photo-863988.jpeg",
            "likes": 0,
            "comments":0
        },
        {
            "title": "My gym buddy watching me try to beat my PR 🏋️‍♂️",
            "image_url": "https://images.pexels.com/photos/1552249/pexels-photo-1552249.jpeg",
            "likes":0,
            "comments":0
        }
    ]
}

def handle_like(meme_id):
    if meme_id not in st.session_state.likes:
        st.session_state.likes[meme_id] = True
        return True
    else:
        st.session_state.likes.pop(meme_id)
        return False

def add_comment(meme_id, comment):
    if meme_id not in st.session_state.comments:
        st.session_state.comments[meme_id] = []
    st.session_state.comments[meme_id].append({
        'text': comment,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def resize_image(image, max_width=MAX_IMAGE_WIDTH, max_height=MAX_IMAGE_HEIGHT):
    """Resize image while maintaining aspect ratio"""
    # Get current dimensions
    width, height = image.size
    
    # Calculate aspect ratio
    aspect_ratio = width / height
    
    # Calculate new dimensions
    if width > max_width or height > max_height:
        if aspect_ratio > 1:
            # Image is wider than tall
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            # Image is taller than wide
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
        
        # Resize image
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return image

def get_image_from_url(url):
    """Download image from URL and return PIL Image object"""
    try:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        return image
    except:
        return None

def convert_image_to_base64(image_file):
    if isinstance(image_file, str):  # If it's a URL
        if image_file.startswith('data:image'):  # Already base64
            return image_file
        
        # Download and resize image from URL
        image = get_image_from_url(image_file)
        if image:
            image = resize_image(image)
            buffered = io.BytesIO()
            image.save(buffered, format=image.format or 'JPEG', quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/jpeg;base64,{img_str}"
        return image_file
    
    # Handle uploaded file
    image = Image.open(image_file)
    image = resize_image(image)
    buffered = io.BytesIO()
    image.save(buffered, format=image.format or 'JPEG', quality=85)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{image.format.lower() if image.format else 'jpeg'};base64,{img_str}"

def share_meme(meme_title, meme_url):
    try:
        # Encode the message
        message = f"Check out this fitness meme: {meme_title}"
        encoded_message = urllib.parse.quote(message)
        
        # Handle both URL and base64 image data
        if meme_url.startswith('data:image'):
            # For uploaded images, we'll just share the title
            encoded_url = ""
        else:
            encoded_url = urllib.parse.quote(meme_url)
        
        # Create sharing links
        whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_message}"
        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_message}"
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_message}"
        instagram_url = "https://www.instagram.com"
        
        # Create columns for social media buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📱 WhatsApp", key=f"whatsapp_{meme_title}"):
                webbrowser.open(whatsapp_url)
                st.toast("Opening WhatsApp...")
        
        with col2:
            if st.button("🐦 Twitter", key=f"twitter_{meme_title}"):
                webbrowser.open(twitter_url)
                st.toast("Opening Twitter...")
        
        with col3:
            if st.button("💼 LinkedIn", key=f"linkedin_{meme_title}"):
                webbrowser.open(linkedin_url)
                st.toast("Opening LinkedIn...")
        
        with col4:
            if st.button("📸 Instagram", key=f"instagram_{meme_title}"):
                webbrowser.open(instagram_url)
                st.toast("Opening Instagram...")
                
    except Exception as e:
        st.error(f"Error sharing meme: {str(e)}")

def display_meme(meme, category_suffix=""):
    with st.container():
        st.markdown(f"#### {meme['title']}")
        
        # Create a container with fixed dimensions
        with st.container():
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; 
                           max-width: {MAX_IMAGE_WIDTH}px; margin: 0 auto;">
                    <img src="{meme['image_url']}" style="max-width: 100%; max-height: {MAX_IMAGE_HEIGHT}px; 
                         object-fit: contain;">
                </div>
                """,
                unsafe_allow_html=True
            )
        
        meme_id = f"{meme['title']}_{category_suffix}"
        col1, col2, col3 = st.columns([1, 1, 3])
        
        # Like button with counter
        with col1:
            is_liked = meme_id in st.session_state.likes
            like_count = meme['likes'] + (1 if is_liked else 0)
            if st.button(
                f"{'❤️' if is_liked else '🤍'} {like_count}", 
                key=f"like_{meme_id}"
            ):
                if handle_like(meme_id):
                    st.toast("Liked!")
                else:
                    st.toast("Unliked!")
                st.rerun()
        
        # Comment section
        with col2:
            if st.button(f"💬 {meme['comments'] + len(st.session_state.comments.get(meme_id, []))}", 
                        key=f"comment_{meme_id}"):
                st.session_state[f"show_comments_{meme_id}"] = True
        
        # Share button
        with col3:
            if st.button("Share on Social Media...", key=f"share_{meme_id}"):
                st.session_state[f"show_share_{meme_id}"] = True
        
        # Share options
        if st.session_state.get(f"show_share_{meme_id}", False):
            share_meme(meme['title'], meme['image_url'])
        
        # Comment display and input
        if st.session_state.get(f"show_comments_{meme_id}", False):
            with st.expander("Comments", expanded=True):
                for comment in st.session_state.comments.get(meme_id, []):
                    st.text(f"{comment['timestamp']}: {comment['text']}")
                
                new_comment = st.text_input("Add a comment", key=f"comment_input_{meme_id}")
                if st.button("Post", key=f"post_{meme_id}"):
                    if new_comment:
                        add_comment(meme_id, new_comment)
                        st.toast("Comment posted!")
                        st.rerun()
                    else:
                        st.warning("Please enter a comment")
        
        st.divider()

def save_uploaded_meme(uploaded_file, caption, category):
    if uploaded_file is not None:
        try:
            # Convert and resize image to base64 for storage and display
            image_data = convert_image_to_base64(uploaded_file)
            
            # Create a new meme entry
            new_meme = {
                "title": caption,
                "image_url": image_data,
                "likes": 0,
                "comments": 0,
                "category": category,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.user_memes.append(new_meme)
            return True
        except Exception as e:
            st.error(f"Error saving meme: {str(e)}")
            return False
    return False

def main():
    # Initialize session state FIRST
    init_session_state()
    check_authenticated()
    # Apply dark theme
    apply_dark_theme()
    
    # Main title with emoji
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: 0;'>
            💪 Fitness Memes That Hit Different
        </h1>
        <p style='text-align: center; color: #888; font-size: 1.2em; margin-bottom: 2em;'>
            Because getting fit doesn't have to be boring
        </p>
    """, unsafe_allow_html=True)
    
    # Category tabs
    tabs = st.tabs(["Motivation", "Nutrition", "Workout", "Your Memes"])
    
    # Motivation tab
    with tabs[0]:
        st.markdown("### Motivation Memes 🔥")
        for meme in MEME_DATABASE["motivation"]:
            display_meme(meme, "mot")
    
    # Nutrition tab
    with tabs[1]:
        st.markdown("### Nutrition Memes 🥗")
        for meme in MEME_DATABASE["nutrition"]:
            display_meme(meme, "nut")
    
    # Workout tab
    with tabs[2]:
        st.markdown("### Workout Memes 🏋️‍♂️")
        for meme in MEME_DATABASE["workout"]:
            display_meme(meme, "work")
    
    # Your Memes tab
    with tabs[3]:
        st.markdown("### Your Memes 📸")
        if st.session_state.user_memes:
            for meme in st.session_state.user_memes:
                display_meme(meme, "user")
        else:
            st.info("Share your first meme using the submission form in the sidebar! 🎯")
    
    # Sidebar with trending and submission
    with st.sidebar:
        st.markdown("### 🔥 Trending")
        st.markdown("1. When the pre-workout hits different")
        st.markdown("2. Rest day? Never heard of her")
        st.markdown("3. Protein shake time!")
        
        st.markdown("### 📤 Submit a Meme")
        with st.form("meme_submission"):
            uploaded_file = st.file_uploader("Upload your meme", type=["jpg", "jpeg", "png", "gif"])
            caption = st.text_input("Add a caption")
            category = st.selectbox("Category", ["Motivation", "Nutrition", "Workout"])
            
            submit_button = st.form_submit_button("Post Meme")
            if submit_button:
                if uploaded_file is None:
                    st.error("Please upload an image")
                elif not caption:
                    st.error("Please add a caption")
                else:
                    if save_uploaded_meme(uploaded_file, caption, category):
                        st.success("Meme posted successfully!")
                        st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("Made with 💪 by FitFusion")

if __name__ == "__main__":
    main() 