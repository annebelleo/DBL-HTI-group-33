from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd

# next command ensures that plots appear inside the notebook
#%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns  # also improves the look of plots
sns.set()  # set Seaborn defaults

def getImage(GRAPH = 'NASDAQ'):
	df_stocks_0 = pd.read_csv('datasets/stocks-monthly.csv',parse_dates=[0])
	df_stocks_0.head()
	df_stocks = df_stocks_0.set_index('Date')
	df_stocks.head()
	ax_nasdaq = df_stocks[GRAPH].plot()
	ax_nasdaq.set_title(("Development of",GRAPH,"Composite index"), size=16, weight='bold')
	ax_nasdaq.set_xlabel('Date')
	ax_nasdaq.set_ylabel("Index")
	ax_nasdaq.legend([GRAPH]);
	ax_nasdaq.get_figure().savefig('static/composite.png')
getImage('NASDAQ')



app = Flask(__name__)

@app.route("/")
def home():
	
	return render_template("index.html", user_image = "static/composite.png" )

if __name__== "__main__":
	app.run()