from flask import Flask,render_template,request,redirect
from main import weatherreport
app = Flask(__name__)
print(__name__)



@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        dicton = weatherreport(data['subject'])
        weather,temp,feel,humidity = dicton['weather'],dicton['temp'],dicton['feel'],dicton['humidity']
        return render_template('index.html',city=data['subject'],weather= weather,temp = temp,feel = feel,humidity = humidity)
    
    else:
        return "sorry,something went wrong"
    
    
       
        
    
        





app.run(debug=True)