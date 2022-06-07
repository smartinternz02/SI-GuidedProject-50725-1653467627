from flask import Flask, render_template, request 
import pickle 
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "hZvyweXuya3oowdRQWKJyWom-ajjelgKNi6d6RuZAoDW"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__) 
 
scalar = pickle.load(open("scalar_movies.pkl","rb")) 
 
@app.route('/') 
def hello(): 
    return render_template("Demo2.html") 
 
@app.route('/resultnew', methods = ['POST']) 
def User(): 
    b = request.form["bg"] 
    c = request.form["ge"] 
    d = request.form["pr"] 
    e = request.form["rt"] 
    f = request.form["va"] 
    g = request.form["vc"]  
    i = request.form["rm"] 
    j = request.form["rd"] 
    t = [[float(b),float(c),float(d),float(e),float(f),float(g),float(i),float(j)]] 
    y = scalar.transform(t) 
    payload_scoring = {"input_data": [{"fields": ['f0','f1','f2','f3','f4','f5','f6','f7'], "values": y}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ae093fd9-d762-4dd4-99f1-da88a5605bb8/predictions?version=2022-06-06', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
   
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0][0]
    return render_template("resultnew.html",out="The revenue is $"+str(output)+" million") 
 
if __name__ == '__main__': 
    app.run(debug = False)
