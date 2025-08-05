from flask import Flask, render_template, request
from app import get_recommendations

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_data = {
            "age": request.form["age"],
            "gender": request.form["gender"],
            "weight": request.form["weight"],
            "height": request.form["height"],
            "veg_or_nonveg": request.form["veg_or_nonveg"],
            "disease": request.form["disease"],
            "region": request.form["region"],
            "allergics": request.form["allergics"],
            "foodtype": request.form["foodtype"]
        }

        restaurant_names, breakfast_names,lunch_names, dinner_names, workout_names = get_recommendations(input_data)

        return render_template("result.html", 
                               restaurant_names=restaurant_names,
                               breakfast_names=breakfast_names,
                                lunch_names=lunch_names,  # new line
                               dinner_names=dinner_names,
                               workout_names=workout_names)

    return render_template("index.html")

