import joblib
import numpy as np
from flask import Flask, request, render_template
from config.paths_config import MODEL_OUTPUT_PATH

# Here the flask code is initialized and all the code below it belongs to the flask code.
app = Flask(__name__) 

# Load the model
loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/', methods=['GET','POST']) # Set a route for the home page
# GET - Get the data from the form in home page 
# POST - To post the prediction result in the home page
def index():
    if request.method == 'POST':

        lead_time = int(request.form['lead_time']) # [name of id in the form]
        no_of_special_requests = int(request.form['no_of_special_requests'])
        avg_price_per_room = float(request.form['avg_price_per_room'])
        arrival_month = int(request.form['arrival_month'])
        arrival_date = int(request.form['arrival_date'])
        market_segment = int(request.form['market_segment_type'])
        no_of_week_nights = int(request.form['no_of_week_nights'])
        no_of_weekend_nights = int(request.form['no_of_weekend_nights'])
        type_of_meal_plan = int(request.form['type_of_meal_plan'])
        room_type_reserved = int(request.form['room_type_reserved'])

        features = np.array([[lead_time, no_of_special_requests, 
                              avg_price_per_room, arrival_month, 
                              arrival_date, market_segment, 
                              no_of_week_nights, no_of_weekend_nights, 
                              type_of_meal_plan, room_type_reserved]])
        
        prediction = loaded_model.predict(features)
        return render_template('index.html', prediction=prediction[0]) # [name of html file in templates folder]

    return render_template('index.html', prediction=None) # [name of html file in templates folder]

    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)

