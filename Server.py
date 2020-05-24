from flask import Flask, render_template, request, session

import pandas as pd
import numpy as np

# Visualation methods.
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from Gazestripes_bokeh import draw_gaze_stripes

app = Flask(__name__)
app.secret_key = "pPAQaAI4lte5d8Hwci1i"

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)

ListStimuliName = np.sort(df_data.StimuliName.unique())
ListUser = np.sort(df_data.user.unique())
ListUser = np.insert(ListUser, 0, "ALL")
ListVISID = ["Gazeplot", "Heatmap", "Transition graph", "Gaze Stripes"]
LISTS = [ListUser, ListStimuliName, ListVISID]


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        for ID in ["MapID", "UserID", "VisID"]:
            if request.form[ID]:
                session[ID] = request.form[ID]
            else:
                return render_template("home.html", session=[], LISTS=LISTS)

        if session["VisID"] == "Gazeplot":
            Graph = draw_gazeplot(session["UserID"], session["MapID"])

        elif session["VisID"] == "Heatmap":
            Graph = draw_heatmap(session["UserID"], session["MapID"])

        elif session["VisID"] == "Transition graph":
            Graph = draw_transition_graph(session["UserID"], session["MapID"])

        elif session["VisID"] == "Gaze Stripes":
            Graph = draw_gaze_stripes(session["UserID"], session["MapID"])

        return render_template("home.html", session=session, LISTS=LISTS, Graph=Graph)
    else:
        return render_template("home.html", session=[], LISTS=LISTS)


@app.route("/help/")
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=False)
