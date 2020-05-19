from flask import Flask, redirect, url_for, render_template, request, session

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import os

# When these are ready they can be commented out.
from bokehtest import testscript
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph


app = Flask(__name__)
app.secret_key = "pPAQaAI4lte5d8Hwci1i"

#def readFile(filename):
    #filehandle = open(filename)
    #print filehandle.read()
    #filehandle.close()

#fileDir = os.path.dirname(os.path.realpath('__file__'))
#print fileDir

#For accessing the file in the same folder
#csv_file = "all_fixation_data_cleaned_up.csv"
#readFile(csv_file)

#For accessing the file in a folder contained in the current folder
#csv_file = os.path.join(fileDir, 'static/all_fixation_data_cleaned_up.csv')
#readFile(filename)

df_data = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding='latin1', delim_whitespace=True)
df_cars = pd.read_csv("cars.csv", encoding='latin1', delim_whitespace=True)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        session["MapID"] = request.form["MapID"]
        session["MapIMG"] = os.path.join('stimuli', request.form["MapID"] + ".jpg")
        session["UserID"] = request.form["UserID"]
        session["VisID"] = request.form["VisID"]

        if int(session["VisID"]) == 1:
            session["Vis1_out"] = draw_gazeplot('p1', '04_Köln_S1.jpg')

        elif int(session["VisID"]) == 2:
            session["Vis1_out"] = draw_heatmap('p9', '01b_Antwerpen_S2.jpg')

        elif int(session["VisID"]) == 3:
            session["Vis1_out"] = draw_transition_graph('04_Köln_S1.jpg')

        elif int(session["VisID"]) == 4:
            session["Vis1_out"] = testscript(df_cars)

        elif int(session["VisID"]) == 5:
            session["Vis1_out"] = testscript(df_cars)
        return render_template("home.html", session=session)
    else:
        return render_template("home.html", session=[])


@app.route("/help/")
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(debug=True)
