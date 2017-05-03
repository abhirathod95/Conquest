from app import app
from flask import render_template, request

@app.route('/fake')
def fake_login():
	if request.args.get("url"):
		url = request.args.get("url")

	return render_template("index.html")

