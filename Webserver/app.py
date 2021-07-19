from flask import Flask, render_template,request
import socket
#import hate_classifier

addr = socket.gethostbyname(socket.gethostname())
info = {'address':addr}

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("all.html",ip_addr=info)

@app.route('/', methods=['POST'])
def welcome():
	if request.method == 'POST':
		text = request.form["des"]
		#predict = hate_classifier.get_prediction(text)
		predict = "demo"
		results= {'ans': predict}
	return render_template("all.html",your_result = results,ip_addr=info)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)