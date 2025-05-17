import streamlit as st
from auth import init_session_state, check_authenticated
import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd
from config import apply_dark_theme

# Try to import optional dependencies
try:
    import cv2
    import mediapipe as mp
    import numpy as np
    from PIL import Image
    CAMERA_ENABLED = True
    
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
except ImportError:
    CAMERA_ENABLED = False

# Dance moves database
# Dance moves database with unique video URLs for each move
DANCE_MOVES = {
    "The Shuffle": {
        "difficulty": "Easy",
        "points": 10,
        "description": "Move your feet side to side while alternating arm movements",
        "tips": ["Keep your upper body relaxed", "Maintain a steady rhythm", "Slide feet smoothly"],
        "video_url": "https://www.youtu.com/embed/cbKkB3POqaY"  # Unique shuffle tutorial
    },
    "Robot Dance": {
        "difficulty": "Easy",
        "points": 15,
        "description": "Make rigid, mechanical movements with your arms and body",
        "tips": ["Keep movements sharp", "Stay in character", "Use right angles"],
        "video_url": "https://www.youtu.com/embed/g_tea8ZNk5A"  # Robot dance tutorial
    },
    "Hip Hop Groove": {
        "difficulty": "Medium",
        "points": 25,
        "description": "Basic hip hop dance moves with rhythm and style",
        "tips": ["Feel the beat", "Keep your knees bent", "Move with confidence"],
        "video_url": "https://www.youtube.com/embed/ujREEgxEP7g"  # Hip hop tutorial
    },
    "Cardio Dance": {
        "difficulty": "Medium",
        "points": 20,
        "description": "High-energy dance workout combining basic steps",
        "tips": ["Keep core engaged", "Stay light on your feet", "Follow the rhythm"],
        "video_url": "https://www.youtube.com/embed/ZWk19OVon2k"  # Cardio dance tutorial
    },
    "Power Dance": {
        "difficulty": "Hard",
        "points": 35,
        "description": "Intense dance workout with dynamic movements",
        "tips": ["Start with basic moves", "Control your breathing", "Stay hydrated"],
        "video_url": "https://www.youtube.com/embed/1f8yoFFdkcY"  # Power dance tutorial
    }
}
 

# Challenge combinations
CHALLENGES = [
    {"name": "Speed Challenge", "description": "Perform the moves as quickly as possible!"},
    {"name": "Smooth Flow", "description": "Connect the moves as smoothly as you can"},
    {"name": "Mirror Match", "description": "Copy the moves while looking in a mirror"},
    {"name": "Eyes Closed", "description": "Try the moves with your eyes closed (be careful!)"},
    {"name": "Reverse Order", "description": "Perform the sequence in reverse"}
]

# Initialize session state
if 'current_score' not in st.session_state:
    st.session_state.current_score = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'battle_history' not in st.session_state:
    st.session_state.battle_history = []
if 'current_move' not in st.session_state:
    st.session_state.current_move = None
if 'battle_active' not in st.session_state:
    st.session_state.battle_active = False

def calculate_pose_similarity(user_pose_landmarks, target_pose_landmarks):
    """Calculate similarity between user's pose and target pose"""
    if user_pose_landmarks and target_pose_landmarks:
        # Simplified similarity calculation
        similarity = random.uniform(0.6, 1.0)  # Placeholder for actual pose comparison
        return similarity
    return 0.0

def analyze_dance_move(frame):
    """Analyze dance move from camera frame"""
    # Convert frame to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    
    if results.pose_landmarks:
        return results.pose_landmarks
    return None

def start_dance_battle():
    """Initialize a new dance battle"""
    st.session_state.current_score = 0
    st.session_state.current_move = random.choice(list(DANCE_MOVES.keys()))
    st.session_state.battle_active = True

def update_score(points):
    """Update the score and high score"""
    st.session_state.current_score += points
    if st.session_state.current_score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.current_score

def save_battle_results():
    """Save battle results to history"""
    st.session_state.battle_history.append({
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'score': st.session_state.current_score,
        'moves_completed': len(st.session_state.battle_history) + 1
    })

def main():
    # Initialize session state FIRST
    init_session_state()
    check_authenticated()
    # Apply dark theme
    apply_dark_theme()
    
    # Main title with custom styling
    st.markdown("""
        <style>
            .title {
                text-align: center;
                color: #FF4B4B;
                margin-bottom: 0.5em;
            }
            .subtitle {
                text-align: center;
                font-size: 1.2em;
                margin-bottom: 1.5em;
            }
            .video-container {
                position: relative;
                padding-bottom: 56.25%;
                height: 0;
                overflow: hidden;
                max-width: 100%;
                background-color: #1E1E1E;
                border-radius: 10px;
                margin: 1em 0;
            }
            .video-container iframe {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 0;
            }
            .move-card {
                padding: 1.5em;
                background-color: #1E1E1E;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 1em;
            }
            .tip-item {
                padding: 0.5em;
                margin: 0.5em 0;
                background-color: #2E2E2E;
                border-radius: 5px;
            }
            .tutorial-box {
                background-color: #1E1E1E;
                padding: 1.5em;
                border-radius: 10px;
            }
        </style>
        
        <h1 class="title">💃 Dance Battle Challenge 🕺</h1>
        <p class="subtitle">Get moving and score points with awesome dance moves!</p>
    """, unsafe_allow_html=True)
    
    # Installation instructions if camera features are not available
    if not CAMERA_ENABLED:
        st.warning("""
            📸 Camera features are not available. To enable full functionality, install required packages:
            ```
            pip install opencv-python mediapipe numpy
            ```
            For now, you can still practice with the video demonstrations!
        """)
    
    # Sidebar with stats and leaderboard
    with st.sidebar:
        st.markdown("### 🏆 Stats")
        st.metric("Current Score", st.session_state.current_score)
        st.metric("High Score", st.session_state.high_score)
        
        if st.session_state.battle_history:
            st.markdown("### 📊 Battle History")
            history_df = pd.DataFrame(st.session_state.battle_history)
            st.line_chart(history_df.set_index('date')['score'])
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not st.session_state.battle_active:
            with st.container():
                st.markdown("### Ready to Battle?")
                st.write("Follow the dance moves and earn points!")
                if st.button("🎮 Start Dance Battle", use_container_width=True):
                    start_dance_battle()
        else:
            # Show video demonstration
            if st.session_state.current_move:
                move = DANCE_MOVES[st.session_state.current_move]
                st.markdown(f"### Current Move: {st.session_state.current_move}")
                st.write("**Watch and follow the demonstration:**")
                
                # Embed YouTube video
                st.markdown(f"""
                    <div class="video-container">
                        <iframe 
                            src="{move['video_url']}"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                    </div>
                """, unsafe_allow_html=True)
            
            if st.button("⏹️ End Battle", use_container_width=True):
                save_battle_results()
                st.session_state.battle_active = False
                st.rerun()
    
    with col2:
        if st.session_state.battle_active and st.session_state.current_move:
            move = DANCE_MOVES[st.session_state.current_move]
            
            # Move info card
            with st.container():
                st.markdown(f"""
                    <div class="move-card">
                        <h3 style='color: #FF4B4B; margin-bottom: 1em;'>Move Details</h3>
                        <p><strong style='color: #FFA07A;'>Difficulty:</strong> {move['difficulty']}</p>
                        <p><strong style='color: #FFA07A;'>Points:</strong> {move['points']}</p>
                        <p style='margin-top: 1em;'>{move['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Tips section
            with st.expander("💡 Tips", expanded=True):
                for tip in move['tips']:
                    st.markdown(f"""
                        <div class="tip-item">
                            • {tip}
                        </div>
                    """, unsafe_allow_html=True)
            
            # Next move button
            if st.button("Next Move ⏭️", use_container_width=True):
                update_score(move['points'])
                st.session_state.current_move = random.choice(list(DANCE_MOVES.keys()))
                st.rerun()
    
    # Tutorial section
# Replace your current tutorial section with this:
with st.expander("❓ How to Play"):
    st.markdown("""
    **Getting Started**  
    1. Click 'Start Dance Battle' to begin  
    2. Watch and follow the video demonstration  
    3. Practice the move using the tips provided  
    4. Click 'Next Move' when ready to continue  
    5. Try to beat your high score!  

    **Tips for Success**  
    - Start with easier moves  
    - Follow the movement tips  
    - Take breaks when needed  
    - Stay hydrated  
    - Have fun and stay energetic!
    """)

if __name__ == "__main__":
    main()