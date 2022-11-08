import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import inputScript

app = Flask(__name__,template_folder='../Flask/static/templates')
model = pickle.load(open('../Flask/Phishing_Website.pkl','rb'))

@app.route('/')
def home():
    return render_template('../Flask/index.html')

@app.route('/predict')
def predict():
    return render_template('Final.html')

ans = ""   
bns = ""   
@app.route('/y_predict', methods=['POST'])
def y_predict():
    url = request.form['URL']
    checkprediction = inputScript.main(url)
    prediction = model.predict(checkprediction)
    print(prediction)
    output=prediction[0]
    if(output==1):
        pred="You are safe!!  This is a legitimate Website."
        return render_template('Final.html',bns=pred)
    
    else:
        pred="You are on the wrong site. Be cautious!"        
        return render_template('Final.html',ans=pred)


@app.route('/predict_api', methods=['POST'])
def predict_api():
    
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output=prediction[0]
    return jsonify(output)        
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
    