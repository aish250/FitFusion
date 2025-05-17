import streamlit as st

def apply_dark_theme():
    # Set dark theme using custom CSS
    st.markdown("""
        <style>
        /* Global text color */
        * {
            color: white !important;
        }
        
        /* Dark theme styles */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        .stButton>button {
            background-color: #4CAF50;
            color: white !important;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
        }
        
        .stButton>button:hover {
            background-color: #45a049;
        }
        
        .stTextInput>div>div>input {
            background-color: #262730;
            color: white !important;
            border: 1px solid #4B4B4B;
        }
        
        .stSelectbox>div>div>select {
            background-color: #262730;
            color: white !important;
            border: 1px solid #4B4B4B;
        }
        
        .stTab {
            background-color: #262730;
            color: white !important;
        }
        
        /* Success message styling */
        .stSuccess {
            background-color: #1E4620;
            color: #4CAF50 !important;
        }
        
        /* Error message styling */
        .stError {
            background-color: #4A1C1C;
            color: #FF4B4B !important;
        }

        /* Additional dark theme elements */
        .stMarkdown {
            color: white !important;
        }
        
        .stSidebar {
            background-color: #0E1117;
        }
        
        .stProgress > div > div {
            background-color: #4CAF50;
        }
        
        .stSlider > div > div {
            background-color: #262730;
        }
        
        .stDataFrame {
            background-color: #262730;
            color: white !important;
        }
        
        .stTable {
            background-color: #262730;
            color: white !important;
        }
        
        /* Card-like containers */
        .css-1r6slb0 {
            background-color: #262730;
            border: 1px solid #4B4B4B;
            padding: 20px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        /* Metric containers */
        .css-1xarl3l {
            background-color: #262730;
        }
        
        /* Charts and plots */
        .js-plotly-plot {
            background-color: #262730;
        }
        
        /* Dropdown menus */
        .stSelectbox > div[data-baseweb="select"] > div {
            background-color: #262730;
            color: white !important;
        }
        
        /* Multiselect */
        .stMultiSelect > div[data-baseweb="select"] > div {
            background-color: #262730;
            color: white !important;
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }

        /* Links */
        a {
            color: #4CAF50 !important;
        }
        a:hover {
            color: #45a049 !important;
        }

        /* Radio buttons */
        .stRadio > div {
            color: white !important;
        }

        /* Checkboxes */
        .stCheckbox > div {
            color: white !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            color: white !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            color: white !important;
        }

        /* Slider */
        .stSlider [data-baseweb="slider"] {
            color: white !important;
        }

        /* Number input */
        .stNumberInput [data-baseweb="input"] {
            color: white !important;
        }

        /* Text area */
        .stTextArea textarea {
            color: white !important;
            background-color: #262730;
        }

        /* Info boxes */
        .stInfo {
            color: white !important;
            background-color: rgba(255, 255, 255, 0.1);
        }

        /* Warning boxes */
        .stWarning {
            background-color: rgba(255, 152, 0, 0.1);
            color: #FFA726 !important;
        }

        /* All text elements */
        p, span, div, label, text {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

def set_page_config():
    st.set_page_config(
        page_title="FitFusion",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.fitfusion.com/help',
            'Report a bug': 'https://www.fitfusion.com/bug',
            'About': 'FitFusion - Your All-in-One Fitness and Wellness Platform'
        }
    ) 