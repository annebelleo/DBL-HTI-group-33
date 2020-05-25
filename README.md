# Eye Movement Visualization Tool

Welcome to our visualization tool! If you want the run the Flask server locally, follow the next steps.
Download the FULL GitHub repository using the green "clone or download" button.
If you have already installed pip and Flask, open the command prompt/terminal on your computer and navigate to the folder where the tool is located (it should have the same name as this repository.) Then, run Server.py using "python Server.py" or other Python execution method.
Open the webpage on http://127.0.0.1:5000/ in your preferred browser.

## File structure:
root:
-Server.py: This is the main python file. It links the HTML files in templates to the python files.
-README.md: File you are looking at now, containing information about the entire repository.
-files with "bokeh": The visualization methods that utilize the Bokeh library, making them interactive. Also applies for Transition_graph.py.
-HelperFunctions.py: allows the visualization methods to use functions that make the production of the visualization more efficient.
Templates: Here are the HTML pages stored that can be used by the flask server.  
-home.html: Homepage of the website.
-help.html: Page containing usage instructions for the web interface of the tool.
-vis5_result.html: This is the page we show the user when they want to use a visualization method.
Static: this is where the CSS & images are stored that can be used by the server.  
-stimuli: all the subway maps provided by the course
-all_fixation_data_cleaned_up.csv: main dataset that contains data pertaining the eye movement on the stimuli. This was provided by the course.
-cars.csv: test data file to ensure the code properly runs
-main.css: styling sheet for the web design
Code snippets visualization tools: tools that are still in progress.
