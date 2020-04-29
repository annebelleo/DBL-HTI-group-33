#1. Import packages
from flask import Flask, flash, redirect, render_template, request,   session, abort,send_from_directory,send_file,jsonify
import pandas as pd
import json


#2. Declare application
app= Flask(__name__)

#3. Create datastore variable
class DataStore():
     CountryName=None
     Year=None
     Prod= None
     Loss=None
data=DataStore()

#We are defining a route along with the relevant methods for the #route, in this case they are get and post.

@app.route("/",methods=["GET","POST"])
