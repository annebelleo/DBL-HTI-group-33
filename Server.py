from flask import Flask, redirect, url_for, render_template, request, session

# Commented these imports when you start using them. As long as there is no code using them leave them commented out.
# import numpy as np
# import pandas as pd
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import seaborn as sns

# When these are ready they can be commented out.
# from Vis_1 import Vis_1
# from Vis_2 import Vis_2
# from Vis_3 import Vis_3
# from Vis_4 import Vis_4
# from Vis_5 import Vis_5

app = Flask(__name__)
app.secret_key = "pPAQaAI4lte5d8Hwci1i"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        session["MapID"] = request.form["MapID"]
        session["UserID"] = request.form["UserID"]
        session["VisID"] = request.form["VisID"]

        # if session["VisID"] == 1: session = VIS_1(session)
        # if session["VisID"] == 2: session = VIS_2(session)
        # if session["VisID"] == 3: session = VIS_3(session)
        # if session["VisID"] == 4: session = VIS_4(session)
        # if session["VisID"] == 5: session = VIS_5(session)

        return render_template("home.html", session=session)
    else:
        return render_template("home.html", session=[])


@app.route("/help/")
def help():
    return render_template("help.html")


""" 
@app.route("/vis5/", methods=["POST", "GET"])
def vis5():
    if request.method == "POST":
        session["boek"] = request.form["nm"]
        return redirect(url_for("vis5result"))
    else:
        return render_template("vis5.html")


@app.route("/vis5/Result/", methods=["POST", "GET"])
def vis5result():
    if "boek" in session:
        #this is where you put the code / function call for your projcet. 
        boek = session["boek"]
        return render_template("vis5_result.html", boek=boek)
    else:
        return redirect(url_for("vis5"))
"""

if __name__ == "__main__":
    app.run(debug=True)
