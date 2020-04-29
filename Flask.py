from flask import Flask, render_template, request, jsonify

## commented these imports when you start using them. As long as there is no code using them leave them commented out.
#import numpy as np
#import pandas as pd
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import seaborn as sns


app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/vis1.")
def vis1():
	return render_template("vis1.html")

@app.route("/vis2.")
def vis2():
	return render_template("vis2.html")

@app.route("/vis3.")
def vis3():
	return render_template("vis3.html")

@app.route("/vis4.")
def vis4():
	return render_template("vis4.html")

@app.route("/vis5.")
def vis5():
	return render_template("vis5.html")

if __name__== "__main__":
	app.run()
	
	
