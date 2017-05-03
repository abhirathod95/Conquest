from app import app
from flask import render_template, request
import sys 
import requests


@app.route('/fake')
def fake_login():
	if request.args.get("url"):
		url = request.args.get("url")
		r = requests.get(url)
		hstring = str(r.text)
		name = "fake.html"
		print(hstring)
		with open("/templates/"+name, 'w') as out:
			out.write(hstring)
	
	return render_template(name)
