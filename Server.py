from flask import Flask, redirect, url_for, render_template, request, session

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# When these are ready they can be commented out.
from bokehtest import testscript
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph


app = Flask(__name__)
app.secret_key = "pPAQaAI4lte5d8Hwci1i"

data_file = pd.read_csv("D:/User/Documenten/GitHub/DBL-HTI-group-33/all_fixation_data_cleaned_up.csv",
                        encoding='latin1', sep='\t')


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        session["MapID"] = request.form["MapID"]
        #session["MapIMG"] = plt.imread('D:/User/Documenten/GitHub/DBL-HTI-group-33/Code snippets visualisation tools/datasets/stimuli/' + request.form["MapID"] + ".jpg")
        session["UserID"] = request.form["UserID"]
        session["VisID"] = request.form["VisID"]

        if int(session["VisID"]) == 1:
            session["Vis1_out"] = draw_gazeplot('p1', '04_Köln_S1.jpg')

        elif int(session["VisID"]) == 2:
            session["Vis1_out"] = draw_heatmap('p9', '01b_Antwerpen_S2.jpg')

        elif int(session["VisID"]) == 3:
            session["Vis1_out"] = draw_transition_graph('04_Köln_S1.jpg')

        elif int(session["VisID"]) == 4:
            session["Vis1_out"] = testscript(pd.read_csv('D:/User/Documenten/GitHub/DBL-HTI-group-33/cars.csv'))

        elif int(session["VisID"]) == 5:
            session["Vis1_out"] = testscript(pd.read_csv('D:/User/Documenten/GitHub/DBL-HTI-group-33/cars.csv'))
        return render_template("home.html", session=session)
    else:
        return render_template("home.html", session=[])


@app.route("/help/")
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(debug=True)
