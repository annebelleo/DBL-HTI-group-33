from flask import Flask, redirect, url_for, render_template, request, session

# Commented these imports when you start using them. As long as there is no code using them leave them commented out.
# import numpy as np
# import pandas as pd
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import seaborn as sns


app = Flask(__name__)
app.secret_key = "pPAQaAI4lte5d8Hwci1i"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/vis1/")
def vis1():
    return render_template("vis1.html")


@app.route("/vis2/")
def vis2():
    return render_template("vis2.html")


@app.route("/vis3/")
def vis3():
    return render_template("vis3.html")


@app.route("/vis4/")
def vis4():
    return render_template("vis4.html")


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


if __name__ == "__main__":
    app.run(debug=True)
