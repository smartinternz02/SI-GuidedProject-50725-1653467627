from flask import Flask, render_template, request 
import pickle 
app = Flask(__name__) 
 
model = pickle.load(open("model_movies.pkl","rb")) 
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
    print(t) 
    y = scalar.transform(t) 
    pred = model.predict(y) 
    return render_template("resultnew.html",out="The revenue is $"+str(pred[0][0])+" million") 
 
if __name__ == '__main__': 
    app.run(debug = True)