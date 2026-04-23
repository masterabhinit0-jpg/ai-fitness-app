import streamlit as st
import datetime

# Function to calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor Equation
def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr

# Function to estimate time for weight change
def estimate_time(current_weight, target_weight, daily_calorie_deficit_surplus):
    weight_difference = abs(target_weight - current_weight)
    calories_needed = weight_difference * 3500  # 1 lb = 3500 calories
    days = calories_needed / daily_calorie_deficit_surplus
    return days

# Main app
st.title("AI Fitness App")

st.header("User Inputs")

# Food intake input
food_intake = st.text_area("Enter your daily food intake (e.g., breakfast: oatmeal, lunch: salad, etc.)")

# Weight input
weight = st.number_input("Enter your current weight (kg)", min_value=30.0, max_value=200.0, step=0.1)

# Additional info for BMR
height = st.number_input("Enter your height (cm)", min_value=100, max_value=250, step=1)
age = st.number_input("Enter your age", min_value=10, max_value=100, step=1)
gender = st.selectbox("Select your gender", ["Male", "Female"])

# Goal
goal = st.selectbox("Do you want to lose or gain weight?", ["Lose", "Gain"])
amount = st.number_input("How much weight (kg)?", min_value=0.1, max_value=50.0, step=0.1)

if st.button("Get Recommendations"):
    if not food_intake or weight == 0 or height == 0 or age == 0:
        st.error("Please fill in all inputs.")
    else:
        # Calculate BMR
        bmr = calculate_bmr(weight, height, age, gender)
        
        # Assume activity level (sedentary for simplicity)
        tdee = bmr * 1.2  # Total Daily Energy Expenditure
        
        # Adjust for goal
        if goal == "Lose":
            daily_calories = tdee - 500  # Deficit for 0.5 kg/week loss
            deficit = 500
        else:
            daily_calories = tdee + 500  # Surplus for 0.5 kg/week gain
            deficit = -500
        
        # Estimate time
        target_weight = weight - amount if goal == "Lose" else weight + amount
        days = estimate_time(weight, target_weight, abs(deficit))
        
        st.header("Recommendations")
        
        # Diet
        st.subheader("Diet Plan")
        st.write(f"Based on your inputs, your estimated daily calorie needs are {daily_calories:.0f} calories.")
        st.write("Suggested foods:")
        if goal == "Lose":
            st.write("- Focus on high-protein, low-carb foods: Chicken, fish, vegetables, fruits.")
            st.write("- Avoid: Sugary drinks, fried foods, excessive carbs.")
            st.write("- Portion: Aim for balanced meals with veggies taking half the plate.")
        else:
            st.write("- Focus on calorie-dense foods: Nuts, avocados, whole grains, lean proteins.")
            st.write("- Include: Healthy fats and carbs for energy.")
            st.write("- Portion: Increase portions gradually.")
        
        # Exercises
        st.subheader("Exercise Plan")
        st.write("Weekly exercise schedule:")
        exercises = {
            "Monday": "Cardio: 30 min brisk walk + Strength: Push-ups and squats",
            "Tuesday": "Yoga: 45 min session",
            "Wednesday": "Cardio: 30 min cycling + Core: Planks",
            "Thursday": "Rest or light walk",
            "Friday": "Strength: Full body workout (dumbbells if available)",
            "Saturday": "Cardio: 45 min run or swim",
            "Sunday": "Rest and recovery"
        }
        for day, ex in exercises.items():
            st.write(f"{day}: {ex}")
        
        # Estimated time
        st.subheader("Estimated Time")
        st.write(f"It may take approximately {days:.0f} days to achieve your goal, assuming consistent adherence.")