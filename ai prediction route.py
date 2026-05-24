@app.route('/predict',methods=['POST'])

def predict():

    score = int(
        request.form['score']
    )

    prediction = model.predict(
        [[score]]
    )

    recommended_hours = round(
        prediction[0],
        1
    )

    return render_template(

        "planner.html",

        recommendation=

        recommended_hours

    )