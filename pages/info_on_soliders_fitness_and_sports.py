import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Soldier Fitness Hub",
    page_icon="🪖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .profile-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #2c3e50;
        margin: 10px 0;
        border-left: 4px solid #2c3e50;
    }
    .sport-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 15px;
        background-color: #2c3e50;
        color: white;
        margin-right: 5px;
        font-size: 12px;
    }
    .progress-table {
        width: 100%;
        border-collapse: collapse;
    }
    .progress-table th {
        background-color: #2c3e50;
        color: white;
        padding: 8px;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Soldier Database
SOLDIER_DB = {
    "Army": {
        "Rajesh Kumar": {
            "rank": "Havaldar",
            "unit": "12th Mechanized Infantry",
            "fitness": {
                "pushups": 52,
                "situps": 58,
                "5km_run": "21:45",
                "score": 92/100
            },
            "sports": ["Cross Country", "Kabaddi"],
            "achievements": ["Army Sports Gold 2023", "Inter-Unit Marathon Champion"]
        },
        "Vikram Singh": {
            "rank": "Subedar",
            "unit": "5th Para",
            "fitness": {
                "pushups": 68,
                "situps": 72,
                "5km_run": "18:30",
                "score": 98/100
            },
            "sports": ["Obstacle Course", "Boxing"],
            "achievements": ["Special Forces Fitness Champion", "Commando Challenge Winner"]
        },
        "Amit Sharma": {
            "rank": "Sepoy",
            "unit": "8th Mountain Division",
            "fitness": {
                "pushups": 45,
                "situps": 50,
                "5km_run": "23:15",
                "score": 85/100
            },
            "sports": ["Skiing", "Mountain Climbing"],
            "achievements": ["High Altitude Endurance Award"]
        },
        "Deepak Yadav": {
            "rank": "Naik",
            "unit": "3rd Artillery Regiment",
            "fitness": {
                "pushups": 55,
                "situps": 60,
                "5km_run": "20:45",
                "score": 90/100
            },
            "sports": ["Weightlifting", "Shot Put"],
            "achievements": ["Army Powerlifting Bronze 2022"]
        }
    },
    "Navy": {
        "Arjun Menon": {
            "rank": "Leading Seaman",
            "unit": "INS Chennai",
            "fitness": {
                "pushups": 48,
                "situps": 52,
                "5km_run": "22:15",
                "score": 89/100
            },
            "sports": ["Swimming", "Rowing"],
            "achievements": ["Navy Regatta Silver Medalist", "Deep Sea Diving Expert"]
        },
        "Rahul Nair": {
            "rank": "Petty Officer",
            "unit": "INS Vikramaditya",
            "fitness": {
                "pushups": 50,
                "situps": 55,
                "5km_run": "21:30",
                "score": 91/100
            },
            "sports": ["Sailing", "Water Polo"],
            "achievements": ["Fleet Swimming Champion"]
        },
        "Suresh Patel": {
            "rank": "Chief Petty Officer",
            "unit": "INS Kochi",
            "fitness": {
                "pushups": 60,
                "situps": 65,
                "5km_run": "19:45",
                "score": 95/100
            },
            "sports": ["Combat Diving", "Kayaking"],
            "achievements": ["Maritime Special Operations Award"]
        }
    },
    "Air Force": {
        "Anil Thakur": {
            "rank": "Sergeant",
            "unit": "No. 1 Squadron",
            "fitness": {
                "pushups": 53,
                "situps": 57,
                "5km_run": "20:15",
                "score": 93/100
            },
            "sports": ["Basketball", "Volleyball"],
            "achievements": ["Inter-Services Basketball Gold"]
        },
        "Sanjay Gupta": {
            "rank": "Flight Lieutenant",
            "unit": "No. 7 Squadron",
            "fitness": {
                "pushups": 58,
                "situps": 62,
                "5km_run": "19:30",
                "score": 96/100
            },
            "sports": ["Squash", "Badminton"],
            "achievements": ["Air Force Sportsman of the Year"]
        },
        "Vijay Malhotra": {
            "rank": "Wing Commander",
            "unit": "No. 15 Squadron",
            "fitness": {
                "pushups": 65,
                "situps": 70,
                "5km_run": "18:15",
                "score": 97/100
            },
            "sports": ["Athletics", "Triathlon"],
            "achievements": ["Iron Man Challenge Winner", "Service Cross for Fitness"]
        }
    },
    "Special Forces": {
        "Ravi Shankar": {
            "rank": "Major",
            "unit": "Para SF",
            "fitness": {
                "pushups": 80,
                "situps": 85,
                "5km_run": "16:45",
                "score": 100/100
            },
            "sports": ["Combat Training", "Martial Arts"],
            "achievements": ["Commando Dagger Award", "International SF Competition Gold"]
        },
        "Karan Kapoor": {
            "rank": "Captain",
            "unit": "MARCOS",
            "fitness": {
                "pushups": 75,
                "situps": 80,
                "5km_run": "17:15",
                "score": 99/100
            },
            "sports": ["Underwater Hockey", "Combat Swimming"],
            "achievements": ["Navy Cross", "Anti-Terrorism Operations Medal"]
        }
    }
}

def display_soldier_profile(branch, name):
    """Show detailed soldier fitness and sports profile"""
    soldier = SOLDIER_DB[branch][name]
    
    st.markdown(f"""
    <div class='profile-card'>
        <h3>{name} ({soldier['rank']})</h3>
        <p><strong>Unit:</strong> {soldier['unit']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fitness Metrics
    with st.expander("📊 Fitness Metrics", expanded=True):
        cols = st.columns(4)
        cols[0].metric("Pushups", soldier['fitness']['pushups'], "vs Army Std: 40")
        cols[1].metric("Situps", soldier['fitness']['situps'], "vs Army Std: 45")
        cols[2].metric("5km Run", soldier['fitness']['5km_run'], "vs Army Std: 25:00")
        cols[3].metric("Fitness Score", f"{soldier['fitness']['score']*100:.1f}/100")
        st.progress(soldier['fitness']['score'])
    
    # Sports Specialization
    with st.expander("🏅 Sports Profile"):
        st.markdown("<strong>Primary Sports:</strong>", unsafe_allow_html=True)
        for sport in soldier['sports']:
            st.markdown(f"<span class='sport-badge'>{sport}</span>", unsafe_allow_html=True)
        
        st.markdown("<br><strong>Training Regimen:</strong>", unsafe_allow_html=True)
        if "Cross Country" in soldier['sports']:
            st.write("- Daily 10km runs with interval training")
        if "Swimming" in soldier['sports']:
            st.write("- 2km open water swims 3x weekly")
        
        st.markdown("<br><strong>Notable Achievements:</strong>", unsafe_allow_html=True)
        for achievement in soldier['achievements']:
            st.write(f"• {achievement}")
    
    # Comparison with standards
    st.markdown("### Military Fitness Standards Comparison")
    standards = {
        "Pushups": {"Army": 40, "Para": 60, "Navy": 35},
        "Situps": {"Army": 45, "Para": 55, "Navy": 40},
        "5km Run": {"Army": "25:00", "Para": "22:00", "Navy": "26:00"}
    }
    
    comparison_df = pd.DataFrame(standards).reset_index()
    st.dataframe(comparison_df, hide_index=True, use_container_width=True)

def home_training_page():
    """Page for aspiring soldiers"""
    st.title("Become a Soldier - Home Training")
    
    with st.expander("🏠 Create Your Program", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            level = st.selectbox("Your Level", ["Beginner", "Intermediate", "Advanced"])
            equipment = st.selectbox("Available Equipment", 
                                   ["Bodyweight only", "Chair", "Water bottles", "Rope"])
        with col2:
            weeks = st.slider("Duration (weeks)", 2, 8, 4)
            start_date = st.date_input("Start Date")
        
        if st.button("Generate Program"):
            # Program generation logic would go here
            st.session_state.program_generated = True
    
    if st.session_state.get("program_generated"):
        st.success("Your 4-Week Home Training Program")
        
        # Sample program data
        program = {
            "Week 1": {
                "Monday": "3x5 pushups, 3x10 squats",
                "Tuesday": "15 min brisk walk",
                "Wednesday": "Rest day",
                "Thursday": "3x5 pushups, 3x10 lunges",
                "Friday": "10 min jog",
                "Saturday": "3x10 situps",
                "Sunday": "Rest day"
            }
            # Additional weeks would be added here
        }
        
        for week, days in program.items():
            with st.expander(week):
                for day, workout in days.items():
                    st.markdown(f"**{day}:** {workout}")
        
        # Progress tracker
        st.markdown("### Track Your Progress")
        progress_data = {
            "Date": [datetime.now().date() + timedelta(days=i) for i in range(7)],
            "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "Workout": list(program["Week 1"].values()),
            "Completed": [False]*7
        }
        progress_df = pd.DataFrame(progress_data)
        
        edited_df = st.data_editor(progress_df, 
                                 hide_index=True,
                                 column_config={
                                     "Completed": st.column_config.CheckboxColumn(
                                         "Done",
                                         help="Mark completed workouts"
                                     )
                                 })
        
        # Download options
        st.download_button(
            "Download Your Program",
            edited_df.to_csv(index=False),
            "soldier_training_program.csv",
            "text/csv"
        )

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Soldier Profiles", "Become a Soldier"])
    
    if page == "Soldier Profiles":
        st.title("Soldier Fitness Records")
        branch = st.selectbox("Select Force", list(SOLDIER_DB.keys()))
        soldier = st.selectbox("Select Soldier", list(SOLDIER_DB[branch].keys()))
        display_soldier_profile(branch, soldier)
    else:
        home_training_page()

if __name__ == "__main__":
    if "program_generated" not in st.session_state:
        st.session_state.program_generated = False
    main()