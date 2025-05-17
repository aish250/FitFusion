import streamlit as st
from datetime import datetime, timedelta
from auth import init_session_state, check_authenticated

# -----------------------------
# Enhanced Food Database with More Items
# -----------------------------
FOOD_DATABASE = {
    "apple": {
        "name": "Apple",
        "calories": 95,
        "protein": 0.5,
        "carbs": 25,
        "fat": 0.3,
        "serving_size": "1 medium apple",
        "image_url": "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce"
    },
    "banana": {
        "name": "Banana",
        "calories": 105,
        "protein": 1.3,
        "carbs": 27,
        "fat": 0.3,
        "serving_size": "1 medium banana",
        "image_url": "https://th.bing.com/th/id/OIP.xW2SAK_9PbhzSXaH_7TTEwHaE8?rs=1&pid=ImgDetMain"
    },
    "rice": {
        "name": "Cooked Rice",
        "calories": 206,
        "protein": 4.3,
        "carbs": 45,
        "fat": 0.4,
        "serving_size": "1 cup cooked rice",
        "image_url": "https://th.bing.com/th/id/R.ce92559d1c32372e36b5fe343ba29daa?rik=nWloR%2baNuuMsXg&riu=http%3a%2f%2fmedia2.onsugar.com%2ffiles%2f2014%2f03%2f25%2f070%2fn%2f1922195%2f62a96c30e6ba6fd2_shutterstock_43165990.jpg.xxxlarge_2x.jpg&ehk=%2f0nJ%2be4Q31zwKEiuupR8sZkITHXuC%2btA9FrLbiOS%2f2s%3d&risl=&pid=ImgRaw&r=0"
    },
    "egg": {
        "name": "Boiled Egg",
        "calories": 78,
        "protein": 6.3,
        "carbs": 0.6,
        "fat": 5.3,
        "serving_size": "1 large egg",
        "image_url": "https://eskipaper.com/images/eggs-1.jpg"
    },
    "chicken_breast": {
        "name": "Chicken Breast",
        "calories": 165,
        "protein": 31,
        "carbs": 0,
        "fat": 3.6,
        "serving_size": "100g",
        "image_url": "https://thecookful.com/wp-content/uploads/2022/11/grilled-chicken-legs-square-01.jpg"
    },
    "oats": {
        "name": "Oats",
        "calories": 389,
        "protein": 16.9,
        "carbs": 66,
        "fat": 6.9,
        "serving_size": "100g",
        "image_url": "https://www.healthbenefitstimes.com/glossary/wp-content/uploads/2020/10/Oats.jpg"
    },
    "milk": {
        "name": "Milk",
        "calories": 149,
        "protein": 7.7,
        "carbs": 11.7,
        "fat": 8,
        "serving_size": "1 cup",
        "image_url": "https://www.organicfacts.net/wp-content/uploads/milk-1-600x450.jpg"
    },
    "mixed_nuts": {
        "name": "Mixed Nuts",
        "calories": 607,
        "protein": 20,
        "carbs": 21,
        "fat": 54,
        "serving_size": "100g",
        "image_url": "https://foodtolive.com/wp-content/uploads/2016/06/Mix_Nuts-1-min.jpg"
    },
    "sweet_potato": {
        "name": "Sweet Potato",
        "calories": 86,
        "protein": 1.6,
        "carbs": 20,
        "fat": 0.1,
        "serving_size": "100g",
        "image_url": "https://th.bing.com/th/id/OIP.7x4Xw6T9G5QyQa1bJ3Q5JQHaE8?rs=1&pid=ImgDetMain"
    },
    "salmon": {
        "name": "Salmon",
        "calories": 208,
        "protein": 20,
        "carbs": 0,
        "fat": 13,
        "serving_size": "100g",
        "image_url": "https://th.bing.com/th/id/OIP.5JQl1XQcJgxQk7mKzLk5JQHaE8?rs=1&pid=ImgDetMain"
    },
    "quinoa": {
        "name": "Quinoa",
        "calories": 120,
        "protein": 4.4,
        "carbs": 21,
        "fat": 1.9,
        "serving_size": "100g cooked",
        "image_url": "https://th.bing.com/th/id/OIP.3Xj4Y3Y1Q4Q7Q9Q7Q9Q9QAHaE8?rs=1&pid=ImgDetMain"
    },
    "greek_yogurt": {
        "name": "Greek Yogurt",
        "calories": 59,
        "protein": 10,
        "carbs": 3.6,
        "fat": 0.4,
        "serving_size": "100g",
        "image_url": "https://th.bing.com/th/id/OIP.5JQl1XQcJgxQk7mKzLk5JQHaE8?rs=1&pid=ImgDetMain"
    }
}

# -----------------------------
# Enhanced Goal-Based Macros
# -----------------------------
GOAL_MACROS = {
    "Muscle Gain": {"protein": 1.6, "carbs": 5, "fat": 1},
    "Weight Loss": {"protein": 1.8, "carbs": 2, "fat": 0.8},
    "Endurance": {"protein": 1.4, "carbs": 6, "fat": 1.2},
    "Maintenance": {"protein": 1.2, "carbs": 3, "fat": 1},
    "Athlete": {"protein": 2.0, "carbs": 7, "fat": 1.5}
}

# -----------------------------
# Enhanced Workout-Food Pairing
# -----------------------------
WORKOUT_FOOD_PAIRING = {
    "Running": {
        "pre": ["banana", "oats", "sweet_potato"],
        "post": ["rice", "chicken_breast", "salmon"],
        "hydration": "500-750ml water with electrolytes"
    },
    "Weightlifting": {
        "pre": ["oats", "egg", "greek_yogurt"],
        "post": ["chicken_breast", "rice", "quinoa"],
        "hydration": "500ml water with BCAA"
    },
    "Yoga": {
        "pre": ["banana", "mixed_nuts", "greek_yogurt"],
        "post": ["apple", "egg", "sweet_potato"],
        "hydration": "Herbal tea or coconut water"
    },
    "Cycling": {
        "pre": ["banana", "oats", "rice"],
        "post": ["rice", "milk", "salmon"],
        "hydration": "Electrolyte drink + water"
    },
    "HIIT": {
        "pre": ["banana", "oats"],
        "post": ["chicken_breast", "sweet_potato"],
        "hydration": "Coconut water + regular water"
    }
}

# -----------------------------
# Enhanced Activity Burn Rate
# -----------------------------
ACTIVITY_BURN_RATE = {
    "Running": {"cal/min": 10, "intensity": "Moderate-High"},
    "Cycling": {"cal/min": 8, "intensity": "Moderate"},
    "Weightlifting": {"cal/min": 6, "intensity": "Moderate"},
    "Yoga": {"cal/min": 4, "intensity": "Low"},
    "HIIT": {"cal/min": 12, "intensity": "High"},
    "Swimming": {"cal/min": 11, "intensity": "High"}
}

# -----------------------------
# Helper Functions
# -----------------------------
def display_food(food_key):
    food = FOOD_DATABASE[food_key]
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(food["image_url"], width=150)
    with col2:
        st.markdown(f"### {food['name']}")
        st.write(f"**Serving Size:** {food['serving_size']}")
        st.write(f"**Calories:** {food['calories']} kcal")
        st.write(f"**Macros:** P: {food['protein']}g | C: {food['carbs']}g | F: {food['fat']}g")
        st.write(f"**Food Group:** {'Protein' if food['protein'] > 10 else 'Carb' if food['carbs'] > 20 else 'Fat' if food['fat'] > 15 else 'Other'}")

def calculate_macros(goal, weight):
    macros = GOAL_MACROS[goal]
    return {
        "protein": macros["protein"] * weight,
        "carbs": macros["carbs"] * weight,
        "fat": macros["fat"] * weight,
        "calories": (macros["protein"] * 4 + macros["carbs"] * 4 + macros["fat"] * 9) * weight
    }

def calculate_calories_burned(workout, duration):
    if workout in ACTIVITY_BURN_RATE:
        return ACTIVITY_BURN_RATE[workout]["cal/min"] * duration
    return 0

def nutrient_timing_coach():
    st.header("⏱ Nutrient Timing Coach")
    
    # Athlete profile
    col1, col2 = st.columns(2)
    with col1:
        sport_type = st.selectbox("Sport Type", 
                                ["Endurance", "Strength", "Team", "Combat", "Precision"])
    with col2:
        body_weight = st.number_input("Body Weight (kg)", min_value=40, max_value=150, value=70)

    # Competition details
    st.subheader("Competition Schedule")
    event_date = st.date_input("Event Date")
    event_time = st.time_input("Event Start Time")
    event_duration = st.selectbox("Event Duration", 
                                ["<30 mins", "30-60 mins", "1-2 hours", "2+ hours"])

    # Generate plan button
    if st.button("Generate Nutrition Plan", type="primary"):
        event_datetime = datetime.combine(event_date, event_time)
        st.success("🎯 Personalized Nutrient Timing Plan")
        
        # Pre-competition nutrition (3 hours before)
        pre_event_time = event_datetime - timedelta(hours=3)
        st.subheader(f"PRE-EVENT ({pre_event_time.strftime('%H:%M')}):")
        if sport_type in ["Endurance", "Team"]:
            st.markdown("""
            - **Slow Carbs:** 60g (1.5 cups oatmeal + berries)
            - **Protein:** 20g (3 eggs or protein shake)
            - **Fats:** 10g (1 tbsp nut butter)
            - **Hydration:** 500ml water with electrolytes
            """)
        else:  # Strength/Combat
            st.markdown("""
            - **Slow Carbs:** 40g (1 cup sweet potato)
            - **Protein:** 30g (chicken breast)
            - **Fats:** 15g (avocado)
            - **Hydration:** 500ml water
            """)

        # During competition (if applicable)
        if event_duration in ["1-2 hours", "2+ hours"]:
            halftime_duration = timedelta(minutes=30) if event_duration == "1-2 hours" else timedelta(minutes=60)
            halftime = event_datetime + halftime_duration
            st.subheader(f"HALF-TIME (~{halftime.strftime('%H:%M')}):")
            st.markdown("""
            - **Fast Carbs:** 30g (banana + sports drink)
            - **Electrolytes:** 500ml with sodium/potassium
            - **Quick Protein:** 10g BCAA if available
            """)

        # Post-competition recovery (1 hour after)
        recovery_time = event_datetime + timedelta(hours=1)
        st.subheader(f"POST-EVENT ({recovery_time.strftime('%H:%M')}):")
        recovery_protein = round(body_weight * 0.4)  # 0.4g/kg body weight
        st.markdown(f"""
        - **Protein:** {recovery_protein}g (whey shake or lean meat)
        - **Fast Carbs:** {body_weight}g (rice cakes + honey)
        - **Hydration:** 1.5L with electrolytes
        - **Recovery:** Include anti-inflammatory foods (berries, turmeric)
        """)

        # Sport-specific tips
        st.subheader("Sport-Specific Tips")
        if sport_type == "Endurance":
            st.info("💡 Add 5g BCAA during long events (>2hrs) and consider caffeine 1 hour before")
        elif sport_type == "Strength":
            st.info("💡 Include 5g creatine in post-event shake and prioritize sleep for recovery")
        elif sport_type == "Team":
            st.info("💡 Sip carb-electrolyte mix throughout (15g/15min) and cool down properly")

def display_workout_nutrition(workout):
    """Show detailed pre/post workout nutrition"""
    if workout in WORKOUT_FOOD_PAIRING:
        pairing = WORKOUT_FOOD_PAIRING[workout]
        
        st.subheader(f"🍽 {workout} Nutrition Guide")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Pre-Workout (1-2 hours before)")
            for food_key in pairing["pre"]:
                if food_key in FOOD_DATABASE:
                    st.markdown(f"- {FOOD_DATABASE[food_key]['name']}")
            st.markdown(f"**Hydration:** {pairing['hydration']}")
        
        with col2:
            st.markdown("### Post-Workout (within 30 min)")
            for food_key in pairing["post"]:
                if food_key in FOOD_DATABASE:
                    st.markdown(f"- {FOOD_DATABASE[food_key]['name']}")
            st.markdown("**Recovery Tip:** Hydrate with electrolytes and prioritize protein")

# -----------------------------
# Main App
# -----------------------------
def main():
    # Initialize session state FIRST
    init_session_state()
    check_authenticated()
    
    st.set_page_config(
        page_title="Nutrient & Workout Planner", 
        layout="wide",
        page_icon="🏋️"
    )
    
    st.title("🏋️‍♀️ Advanced Nutrient & Workout Planner")

    # Sidebar - User Profile
    with st.sidebar:
        st.header("Your Fitness Profile")
        goal = st.selectbox("Select your goal:", list(GOAL_MACROS.keys()))
        weight = st.slider("Enter your weight (kg):", 30, 150, 70)
        activity_level = st.select_slider("Activity Level:", 
                                        ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
        
        macros = calculate_macros(goal, weight)
        
        st.markdown("---")
        st.subheader("🎯 Daily Targets")
        st.write(f"**Calories:** {macros['calories']:.0f} kcal")
        st.write(f"**Protein:** {macros['protein']:.1f}g")
        st.write(f"**Carbs:** {macros['carbs']:.1f}g")
        st.write(f"**Fat:** {macros['fat']:.1f}g")
        st.markdown("---")
        
        st.subheader("💡 Quick Tips")
        st.markdown("""
        - Eat protein every 3-4 hours
        - Hydrate well before workouts
        - Post-workout nutrition is crucial
        """)

    # Main Content Area
    tab1, tab2, tab3 = st.tabs(["Workout Nutrition", "Food Database", "Nutrient Timing"])

    with tab1:
        st.header("💪 Workout Nutrition Planner")
        
        col1, col2 = st.columns(2)
        with col1:
            workout = st.selectbox("Select Workout:", list(WORKOUT_FOOD_PAIRING.keys()))
            duration = st.slider("Duration (minutes):", 5, 180, 30)
            
            if workout:
                calories_burned = calculate_calories_burned(workout, duration)
                st.metric("Calories Burned", f"{calories_burned} kcal")
                
                intensity = ACTIVITY_BURN_RATE.get(workout, {}).get("intensity", "N/A")
                st.write(f"**Intensity:** {intensity}")
        
        with col2:
            if workout:
                display_workout_nutrition(workout)
        
        st.markdown("---")
        st.subheader("Calorie Balance Tracker")
        food_input = st.text_input("Enter food consumed:")
        if st.button("Calculate Balance"):
            food_key = food_input.strip().lower().replace(" ", "_")
            if food_key in FOOD_DATABASE:
                food = FOOD_DATABASE[food_key]
                balance = calories_burned - food['calories']
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Burned", f"{calories_burned} kcal")
                col2.metric("Consumed", f"{food['calories']} kcal")
                col3.metric("Balance", 
                           f"{balance} kcal", 
                           "Surplus" if balance < 0 else "Deficit")
            else:
                st.warning("Food not found. Try common items like 'apple' or 'chicken'.")

    with tab2:
        st.header("🍏 Food Nutrition Database")
        
        search_col, display_col = st.columns(2)
        with search_col:
            food_search = st.selectbox("Browse Foods:", 
                                      [""] + sorted([food["name"] for food in FOOD_DATABASE.values()]))
            
            if food_search:
                food_key = next(key for key, val in FOOD_DATABASE.items() if val["name"] == food_search)
                display_food(food_key)
        
        with display_col:
            st.subheader("Food Categories")
            category = st.radio("Browse by Category:", 
                               ["All", "Protein", "Carbs", "Fats", "Dairy", "Grains"])
            
            filtered_foods = []
            if category == "All":
                filtered_foods = FOOD_DATABASE.values()
            else:
                for food in FOOD_DATABASE.values():
                    if category == "Protein" and food["protein"] > 10:
                        filtered_foods.append(food)
                    elif category == "Carbs" and food["carbs"] > 20:
                        filtered_foods.append(food)
                    elif category == "Fats" and food["fat"] > 15:
                        filtered_foods.append(food)
                    elif category == "Dairy" and "milk" in food["name"].lower() or "yogurt" in food["name"].lower():
                        filtered_foods.append(food)
                    elif category == "Grains" and ("rice" in food["name"].lower() or "oats" in food["name"].lower() or "quinoa" in food["name"].lower()):
                        filtered_foods.append(food)
            
            st.write(f"Showing {len(filtered_foods)} items:")
            for food in filtered_foods:
                st.markdown(f"- **{food['name']}** ({food['serving_size']}, {food['calories']} kcal)")

    with tab3:
        nutrient_timing_coach()

if __name__ == "__main__":
    main()