from flask import Flask, flash, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import random as random
import pandas as pd
import datetime

# visualization methods.
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from Gazestripes_bokeh import draw_gaze_stripes
from AOI_rivers_bokeh import draw_AOI_rivers
from AllPlots_bokeh import draw_all_plots
from Data_bokeh import draw_dataframe

# 'library' created by the team to help with he processing of the data
from HelperFunctions import drop_down_info, cleanup

# Initialize the flask server and the encryption key for session data.
UPLOAD_FOLDER = '/TEMP'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "pPAQaAI4lte5d8Hwci1i"

# Read the Fixation data, This should become a non static part of the code.
FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)
translate = {'KÃ¶ln': 'Köln', 'BrÃ¼ssel': 'Brüssel', 'DÃ¼sseldorf': 'Düsseldorf', 'GÃ¶teborg': 'Göteborg',
        'ZÃ¼rich': 'Zürich'}
df_data.replace(translate, regex=True, inplace=True)

# The visualization methods we support in this app.
LIST_VIS_ID = ["Data table", "Gazeplot", "Heatmap", "Transition graph", "Gaze Stripes", "AOI Rivers", "All tools"]


@app.route("/", methods=["POST", "GET"])
def home():
    """

    :return: The web page to be renderd.
    """

    try:
        if session["dataset"]:
            data = pd.read_csv(session["dataset"], encoding='latin1', delim_whitespace=True)
            dropdown = drop_down_info(LIST_VIS_ID, data)
    except:
        dropdown = drop_down_info(LIST_VIS_ID, df_data)

    if request.method == "POST":
        for ID in ["MapID", "UserID", "VisID", "AOInum"]:
            if request.form[ID]:
                session[ID] = request.form[ID]
            else:
                return render_template("home.html", session=[], LISTS=dropdown)
        session["VisID"] = request.form.getlist('VisID') 
        
        if session["VisID"] == "Gazeplot":
            if isinstance(draw_gazeplot(session["UserID"], session["MapID"]), str):
                Graph = False
                output_graph = "There is no data available for this user and map."
            else:
                Graph = draw_gazeplot(session["UserID"], session["MapID"])

        Graph = draw_all_plots(session["UserID"], session["MapID"], session["VisID"], session["AOInum"])
    
        if Graph == False:
            return render_template("home.html", text=output_graph, session=session, LISTS=dropdown, Graph=[])
        else:
            return render_template("home.html", session=session, LISTS=dropdown, Graph=Graph)
    else:
        return render_template("home.html", session=[], LISTS=dropdown)


@app.route("/help/")
def help():
    """

    :return: The web page to be renderd.
    """
    return render_template("help.html")


@app.route("/upload/", methods=["POST", "GET"])
def upload():
    """

    :return: The web page to be renderd.
    """
    print (1)
    if request.method == "POST":
        cleanup(60)
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
            return redirect(request.url)
        if file_ds and file_st:

            chars = "0123456789"
            date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-")
            digits = "".join(random.choice(chars) for _ in range(6))
            fileid = date + digits + "_"

            filename_ds = "TEMP/" + fileid + secure_filename(file_ds.filename)
            file_ds.save(filename_ds)
            session["dataset"] = filename_ds
            file_ds.close()

            filename_st = "TEMP/" + fileid + secure_filename(file_st.filename)
            file_st.save(filename_st)
            session["stimuli"] = filename_st
            file_st.close()
            return redirect("/")

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
