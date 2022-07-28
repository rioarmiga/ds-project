from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# initiate model & columns
LABEL = ["Stay", "Resign"]
with open("model_final.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def welcome():
    return "<h3>Selamat Datang di Program Backend Model Saya</h3>"

@app.route("/predict", methods=["GET", "POST"])
def predict_titanic():
    if request.method == "POST":
        content = request.json
        try:
            new_data = {'Education': content['education'],
                        'JoiningYear': content['join_year'],
                        'City' : content['city'],
                        'PaymentTier' : content['payment_tier'],
                        'Age' : content['age'],
                        'Gender' : content['gender'],
                        'EverBenched' : content['ever_benched'],
                        'ExperienceInCurrentDomain' : content['experience']
                        }
            new_data = pd.DataFrame([new_data])
            res = model.predict(new_data)
            result = {'class':str(res[0]),
                      'class_name':LABEL[res[0]]}
            response = jsonify(success=True,
                               result=result)
            return response, 200
        except Exception as e:
            response = jsonify(success=False,
                               message=str(e))
            return response, 400
    # return dari method get
    return "<p>Silahkan gunakan method POST untuk mode <em>inference model</em></p>"

# app.run(debug=True)