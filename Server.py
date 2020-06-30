from flask import Flask, flash, render_template, request, session, redirect
from werkzeug.utils import secure_filename
import random as random
import pandas as pd
import datetime
import zipfile
import os
import shutil

# visualization methods.
from AllPlots_bokeh import draw_all_plots

# 'library' created by the team to help with he processing of the data
from HelperFunctions import drop_down_info, cleanup_temp_files

# Initialize the flask server and the encryption key for session data.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/TEMP'
UPLOAD_FOLDER = 'static/TEMP/'
app.secret_key = "f37ae97e5c82a986c02a8839e92ac45a"

# Read the Fixation data, This should become a non static part of the code.
FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
DF_DATA = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)
TRANSLATE = {'KÃ¶ln': 'Köln', 'BrÃ¼ssel': 'Brüssel', 'DÃ¼sseldorf': 'Düsseldorf', 'GÃ¶teborg': 'Göteborg',
             'ZÃ¼rich': 'Zürich'}
DF_DATA.replace(TRANSLATE, regex=True, inplace=True)

# The visualization methods we support in this app.
LIST_VIS_ID = ["Data table", "Gazeplot", "Heatmap", "Transition graph", "Gaze Stripes", "AOI Rivers", "AOI Stimulus",
               "All tools"]


@app.route("/", methods=["POST", "GET"])
def home():
    """
    :return: The web page to be rendered.
    """
    try:
        session["del_req"] = bool(request.form["del_req"])
    except:
        session["del_req"] = False

    if request.method == "POST" and session["del_req"] == True:
        os.remove(session["dataset"])
        os.remove(session["stimuli"] + ".zip")
        shutil.rmtree(session["stimuli"])
        session["del_req"] = False

    try:  # to read a user provide dataset
        data = pd.read_csv(session["dataset"], encoding='latin1', delim_whitespace=True)
        session["custom"] = True
    except:
        data = DF_DATA
        session["custom"] = False
        for i in ("dataset", "stimuli", "MapID", "UserID", "VisID", "AOInum"):
            session.pop(i, False)
    finally:  # populate the drop down menus with the appropriate information.
        dropdown = drop_down_info(LIST_VIS_ID, data)

    if request.method == "POST":
        # check that every field has been filled out.
        for ID in ["MapID", "UserID", "VisID", "AOInum"]:
            try:
                session[ID] = request.form[ID]
            except:
                return render_template("home.html", session=session, LISTS=dropdown)

        # We want the list version of VisID instead of a string version.
        # The string version above is enough to check that the data is present
        session["VisID"] = request.form.getlist('VisID')

        try:
            img_loc = session["stimuli"] + "/"
        except:
            img_loc = 'static/stimuli/'

        # Draw all plots with the session data.
        delta_start = datetime.datetime.now()
        graph = draw_all_plots(session["UserID"], session["MapID"], session["VisID"],
                               session["AOInum"], data, img_loc)
        delta_end = datetime.datetime.now()
        print(session["VisID"])
        print("Delta:", delta_end - delta_start)

        return render_template("home.html", session=session, LISTS=dropdown, Graph=graph)
    else:  # request.method == "GET"
        return render_template("home.html", session=session, LISTS=dropdown,
                               Graph=["Please fill out all of the information on the left.", ""])


@app.route("/help/")
def help():
    return render_template("help.html")


@app.route("/upload/", methods=["POST", "GET"])
def upload():
    """

    :return: The web page to be renderd.
    """

    if request.method == "POST":
        cleanup_temp_files(path=UPLOAD_FOLDER, t=7200)  # cleanup uploaded files that are older than t seconds
        # check if the post request has the file part
        if 'dataset' not in request.files or 'stimuli' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_ds = request.files['dataset']
        file_st = request.files['stimuli']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file_ds.filename == '' or file_st.filename == '':
            flash('No selected file')
            return redirect(r5equest.url)
        if file_ds and file_st:
            chars = "0123456789"
            date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-")
            digits = "".join(random.choice(chars) for _ in range(6))
            fileid = date + digits + "_"

            filename_ds = UPLOAD_FOLDER + fileid + secure_filename(file_ds.filename)
            file_ds.save(filename_ds)
            session["dataset"] = filename_ds
            file_ds.close()

            filename_st = UPLOAD_FOLDER + fileid + secure_filename(file_st.filename)
            file_st.save(filename_st)
            session["stimuli"] = filename_st[:-4]
            file_st.close()

            with zipfile.ZipFile(filename_st, 'r') as zip_ref:
                zip_ref.extractall(session["stimuli"])

            return redirect("/")

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
