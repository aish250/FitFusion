
import streamlit as st
from auth import init_session_state, login_user, logout_user, create_user
from config import set_page_config, apply_dark_theme

def show_login_page():
    st.title("🔐 Login / Sign Up")
    
    # Create tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # Login Tab
    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if login_username and login_password:
                success, message = login_user(login_username, login_password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")
    
    # Sign Up Tab
    with tab2:
        st.header("Create New Account")
        new_username = st.text_input("Username", key="new_username")
        new_password = st.text_input("Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        email = st.text_input("Email")
        
        if st.button("Sign Up", key="signup_button"):
            if new_username and new_password and confirm_password and email:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                elif '@' not in email or '.' not in email:
                    st.error("Please enter a valid email address")
                else:
                    success, message = create_user(new_username, new_password, email)
                    if success:
                        st.success(message)
                        # Automatically log in the user
                        login_user(new_username, new_password)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def main():
    # Apply page configuration and dark theme
    set_page_config()
    apply_dark_theme()
    
    init_session_state()
    
    # Main title always visible
    st.title("🏋️‍♂️ FitFusion")
    st.subheader("Your All-in-One Fitness and Wellness Platform")
    
    # Show logout button in sidebar if user is logged in
    if st.session_state.logged_in:
        st.sidebar.success(f"Welcome, {st.session_state.username}! 🎉")
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
    
    # Main content
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    # Sidebar navigation for logged-in users
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature",
        ["Home", "Nutrient Tracker", "Fitness Quiz", "Fitness Memes", 
         "Emoji Workout", "Mood Music Match", "Depression Therapy", 
         "Dance Battle", "Soldier Fitness"]  # Added new option here
    )

    # Page routing for logged-in users
    if page == "Home":
        st.write("""
        ## Welcome to FitFusion! 
        
        Choose a feature from the sidebar to get started:
        
        - 🍎 **Nutrient Tracker**: Track your daily nutrition
        - 😄 **Fitness Memes**: Enjoy fitness-related memes
        - 💭 **Depression Therapy**: AI-powered emotional support
        - 💃 **Dance Battle**: Interactive dance challenges
        - 🪖 **Soldier Fitness**: Military personnel fitness tracking  # Added new description
        """)
    elif page == "Nutrient Tracker":
        from pages.nutrient_tracker import main as nutrient_tracker_main
        nutrient_tracker_main()
    
    elif page == "Fitness Memes":
        from pages.fitness_memes import main as fitness_memes_main
        fitness_memes_main()
    elif page == "Emoji Workout":
        from pages.emoji_workout import main as emoji_workout_main
        emoji_workout_main()
    
    elif page == "Depression Therapy":
        from pages.depression_therapy import main as depression_therapy_main
        depression_therapy_main()
    elif page == "Dance Battle":
        from pages.dance_battle import main as dance_battle_main
        dance_battle_main()
    elif page == "Soldier Fitness":  # Added new page routing
        from pages.info_on_soldiers_fitness import main as soldier_fitness_main
        soldier_fitness_main()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ by FitFusion Team")

if __name__ == "__main__":
    main()