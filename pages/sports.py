import streamlit as st
from auth import init_session_state, check_authenticated
import streamlit as st
import random
from datetime import datetime
import pandas as pd
from config import apply_dark_theme

# Initialize session state
if 'workout_history' not in st.session_state:
    st.session_state.workout_history = []
if 'performance_metrics' not in st.session_state:
    st.session_state.performance_metrics = {}
if 'current_workout' not in st.session_state:
    st.session_state.current_workout = None

# Sports database
SPORTS_WORKOUTS = {
    "Basketball 🏀": {
        "exercises": {
            "Box Jumps": {"sets": 4, "reps": "12 reps", "focus": "Explosiveness"},
            "Lateral Slides": {"sets": 3, "reps": "30 sec/side", "focus": "Agility"},
            "Free Throw Routine": {"sets": 5, "reps": "10 shots", "focus": "Accuracy"}
        },
        "key_metrics": ["Vertical Jump (in)", "Sprint Time (40m)", "3-Point %"],
        "training_focus": ["Explosiveness", "Agility", "Shooting"]
    },
    "Soccer ⚽": {
        "exercises": {
            "Suicide Sprints": {"sets": 6, "reps": "40m", "focus": "Speed"},
            "Cone Dribbles": {"sets": 4, "reps": "1 min", "focus": "Ball Control"},
            "Wall Pass Drills": {"sets": 3, "reps": "50 passes", "focus": "Accuracy"}
        },
        "key_metrics": ["5km Run Time", "Shot Power (km/h)", "Dribble Speed (sec)"],
        "training_focus": ["Endurance", "Technique", "Power"]
    },
    "Tennis 🎾": {
        "exercises": {
            "Serve Practice": {"sets": 5, "reps": "20 serves", "focus": "Power"},
            "Footwork Ladder": {"sets": 3, "reps": "2 min", "focus": "Agility"},
            "Backhand Drills": {"sets": 4, "reps": "30 strokes", "focus": "Technique"}
        },
        "key_metrics": ["Serve Speed (km/h)", "Reaction Time (ms)", "Stamina Index"],
        "training_focus": ["Serve", "Footwork", "Strokes"]
    },
    "Swimming 🏊": {
        "exercises": {
            "Freestyle Intervals": {"sets": 8, "reps": "50m", "focus": "Endurance"},
            "Flip Turn Practice": {"sets": 10, "reps": "5 turns", "focus": "Technique"},
            "Underwater Kicks": {"sets": 4, "reps": "15m", "focus": "Power"}
        },
        "key_metrics": ["50m Time", "Stroke Count", "Turn Efficiency"],
        "training_focus": ["Freestyle", "Turns", "Dolphin Kick"]
    },
    "Running 🏃": {
        "exercises": {
            "Hill Repeats": {"sets": 6, "reps": "200m", "focus": "Power"},
            "Tempo Run": {"sets": 1, "reps": "20 min", "focus": "Endurance"},
            "Stride Drills": {"sets": 4, "reps": "100m", "focus": "Form"}
        },
        "key_metrics": ["5K Time", "VO2 Max", "Cadence (spm)"],
        "training_focus": ["Speed", "Endurance", "Form"]
    },
    "Cycling 🚴": {
        "exercises": {
            "Hill Climbs": {"sets": 5, "reps": "2 min", "focus": "Power"},
            "Sprint Intervals": {"sets": 8, "reps": "30 sec", "focus": "Speed"},
            "Cadence Drills": {"sets": 3, "reps": "5 min", "focus": "Efficiency"}
        },
        "key_metrics": ["FTP (watts)", "Max Speed (km/h)", "Climb Time (5%)"],
        "training_focus": ["Climbing", "Sprinting", "Endurance"]
    },
    "Boxing 🥊": {
        "exercises": {
            "Heavy Bag Rounds": {"sets": 3, "reps": "3 min", "focus": "Power"},
            "Speed Bag": {"sets": 4, "reps": "2 min", "focus": "Hand Speed"},
            "Footwork Drills": {"sets": 5, "reps": "1 min", "focus": "Agility"}
        },
        "key_metrics": ["Punch Speed (mph)", "Stamina Rounds", "Reaction Time"],
        "training_focus": ["Power", "Speed", "Footwork"]
    },
    "Volleyball 🏐": {
        "exercises": {
            "Block Jumps": {"sets": 5, "reps": "15 jumps", "focus": "Vertical"},
            "Serve Practice": {"sets": 4, "reps": "20 serves", "focus": "Accuracy"},
            "Dig Drills": {"sets": 3, "reps": "50 reps", "focus": "Reaction"}
        },
        "key_metrics": ["Jump Height (in)", "Serve Speed (km/h)", "Dig Accuracy %"],
        "training_focus": ["Jumping", "Serving", "Defense"]
    }
}

def generate_workout(sport, focus_areas):
    if sport not in SPORTS_WORKOUTS:
        return None
    
    exercises = [
        (name, details) 
        for name, details in SPORTS_WORKOUTS[sport]["exercises"].items()
        if details["focus"] in focus_areas
    ]
    
    return {
        "sport": sport,
        "exercises": random.sample(exercises, min(3, len(exercises))),
        "metrics": SPORTS_WORKOUTS[sport]["key_metrics"]
    }

def save_metric(metric, value):
    if metric not in st.session_state.performance_metrics:
        st.session_state.performance_metrics[metric] = []
    
    st.session_state.performance_metrics[metric].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "value": value
    })
    st.success(f"{metric} saved!")

def main():
    # Initialize session state FIRST
    init_session_state()
    check_authenticated()
    apply_dark_theme()
    
    st.title("🏆 Sports Performance Training")
    
    # Sport selection
    sport = st.radio("Select your sport:", 
                    list(SPORTS_WORKOUTS.keys()), 
                    horizontal=True)
    
    # Focus areas
    focus_options = SPORTS_WORKOUTS[sport]["training_focus"]
    focus_areas = st.multiselect(
        "Select focus areas:", 
        focus_options,
        default=focus_options[:1]
    )
    
    # Generate workout
    if st.button("Generate Workout Plan"):
        if not focus_areas:
            st.warning("Please select at least one focus area")
        else:
            st.session_state.current_workout = generate_workout(sport, focus_areas)
    
    # Display current workout
    if st.session_state.current_workout:
        workout = st.session_state.current_workout
        
        st.subheader(f"{workout['sport']} Workout")
        for name, details in workout["exercises"]:
            with st.expander(f"🏋 {name}"):
                st.write(f"*Sets:* {details['sets']}")
                st.write(f"*Reps:* {details['reps']}")
                st.write(f"*Focus:* {details['focus']}")
        
        # Performance tracking form
        with st.form("performance_form"):
            st.subheader("Track Your Performance")
            metric_values = {}
            
            for metric in workout["metrics"]:
                metric_values[metric] = st.number_input(
                    f"Enter your {metric}:",
                    key=f"input_{metric}"
                )
            
            if st.form_submit_button("Save Metrics"):
                for metric, value in metric_values.items():
                    if value:  # Only save if value was entered
                        save_metric(metric, value)
                
                # Add to workout history
                st.session_state.workout_history.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "sport": sport,
                    "focus": focus_areas,
                    "metrics": metric_values
                })
                st.balloons()
                st.success("Workout completed!")
    
    # Progress tracking in sidebar
    with st.sidebar:
        st.header("Your Progress")
        
        if st.session_state.performance_metrics:
            st.subheader("Performance History")
            for metric, values in st.session_state.performance_metrics.items():
                if values:  # Only show if there are values
                    st.write(f"{metric}")
                    df = pd.DataFrame(values)
                    st.line_chart(df.set_index("date"))
        
        if st.session_state.workout_history:
            st.subheader("Recent Workouts")
            for workout in reversed(st.session_state.workout_history[-3:]):
                st.write(f"{workout['date']}")
                st.write(f"Sport: {workout['sport']}")
                st.write(f"Focus: {', '.join(workout['focus'])}")
                st.write("---")

if __name__ == "__main__":

    main()