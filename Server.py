from flask import Flask, redirect, url_for, render_template, request, session


import pandas as pd

# Visualation methods.
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from bokehtest import testscript

app = Flask(__name__)
app.secret_key = "pPAQaAI4lte5d8Hwci1i"

df_data = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding='latin1', delim_whitespace=True)
df_cars = pd.read_csv("cars.csv", encoding='latin1', delim_whitespace=True)

ListStimuliName = df_data.StimuliName.unique()
ListUser = df_data.user.unique()
ListVISID = ["gazeplot", "heatmap", "transition_graph", "Cars"]
LISTS = [ListUser, ListStimuliName, ListVISID]


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        for ID in ["MapID", "UserID", "VisID"]:
            if request.form[ID]:
                session[ID] = request.form[ID]
            else:
                return render_template("home.html", session=[], LISTS=LISTS)

        if session["VisID"] == "gazeplot":
            session["Vis1_out"] = draw_gazeplot(session["UserID"], session["MapID"],)

        elif session["VisID"] == "heatmap":
            session["Vis1_out"] = draw_heatmap(session["UserID"], session["MapID"])

        elif session["VisID"] == "transition_graph":
            session["Vis1_out"] = draw_transition_graph(session["MapID"])

        elif session["VisID"] == "Cars":
            session["Vis1_out"] = testscript(df_cars)

        return render_template("home.html", session=session, LISTS=LISTS)
    else:
        return render_template("home.html", session=[], LISTS=LISTS)


@app.route("/help/")
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(debug=True)
