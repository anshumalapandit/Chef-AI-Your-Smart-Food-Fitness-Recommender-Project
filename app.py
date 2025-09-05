from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
import re

app = Flask(__name__)

llm_resto = ChatGroq(
    api_key = os.environ.get("GROQ_API_KEY"),
    model = "llama-3.3-70b-versatile",
    temperature=0.0
)

# Updated prompt
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region',
                     'allergics', 'foodtype', 'activity_level', 'fitness_goal', 'cuisine',
                     'meal_time', 'sleep_hours', 'water_intake'],
    template=(
        "Diet Recommendation System:\n"
        "I want you to provide output in the following format using the input criteria:\n\n"
        "Restaurants:\n"
        "- name1\n- name2\n- name3\n- name4\n- name5\n- name6\n\n"
        "Breakfast:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n- item6\n\n"
        "Lunch:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n- item6\n\n"
        "Dinner:\n"
        "- item1\n- item2\n- item3\n- item4\n- item5\n\n"
        "Workouts:\n"
        "- workout1\n- workout2\n- workout3\n- workout4\n- workout5\n- workout6\n\n"
        "Criteria:\n"
        "Age: {age}, Gender: {gender}, Weight: {weight} kg, Height: {height} ft, "
        "Vegetarian: {veg_or_nonveg}, Disease: {disease}, Region: {region}, "
        "Allergics: {allergics}, Food Preference: {foodtype}, Activity Level: {activity_level}, "
        "Fitness Goal: {fitness_goal}, Preferred Cuisine: {cuisine}, Meal Preference: {meal_time}, "
        "Sleep Hours: {sleep_hours}, Water Intake: {water_intake}.\n"
    )
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == "POST":
        # Collect all inputs
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_nonveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']
        activity_level = request.form['activity_level']
        fitness_goal = request.form['fitness_goal']
        cuisine = request.form['cuisine']
        meal_time = request.form['meal_time']
        sleep_hours = request.form['sleep_hours']
        water_intake = request.form['water_intake']

        # Input dict
        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'veg_or_nonveg': veg_or_nonveg,
            'disease': disease,
            'region': region,
            'allergics': allergics,
            'foodtype': foodtype,
            'activity_level': activity_level,
            'fitness_goal': fitness_goal,
            'cuisine': cuisine,
            'meal_time': meal_time,
            'sleep_hours': sleep_hours,
            'water_intake': water_intake
        }

        chain = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
        results = chain.run(input_data)

        # Extract sections
        restaurant_names = re.findall(r'Restaurants:\s*(.*?)\n\n', results, re.DOTALL)
        breakfast_names = re.findall(r'Breakfast:\s*(.*?)\n\n', results, re.DOTALL)
        lunch_names = re.findall(r'Lunch:\s*(.*?)\n\n', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:\s*(.*?)\n\n', results, re.DOTALL)
        workout_names = re.findall(r'Workouts:\s*(.*?)\n\n', results, re.DOTALL)

        def clean_list(block):
            return [line.strip("- ") for line in block.strip().split("\n") if line.strip()]

        restaurant_names = clean_list(restaurant_names[0]) if restaurant_names else []
        breakfast_names = clean_list(breakfast_names[0]) if breakfast_names else []
        lunch_names = clean_list(lunch_names[0]) if lunch_names else []
        dinner_names = clean_list(dinner_names[0]) if dinner_names else []
        workout_names = clean_list(workout_names[0]) if workout_names else []

        return render_template('result.html',
                               restaurant_names=restaurant_names,
                               breakfast_names=breakfast_names,
                                lunch_names=lunch_names,
                               dinner_names=dinner_names,
                               workout_names=workout_names)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
