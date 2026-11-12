from flask import Flask, session,render_template, request

import os
import swimclub

print("Loaded swimclub from:", swimclub.__file__)

app = Flask(__name__)
app.secret_key="You will never guess this secret key"

@app.get("/")
def index():
    return render_template(
        "index.html",
        title="Hare Krishna from Swim Club System",
    )

def populate_data():
    if "swimmers" not in session:
        swim_files=os.listdir(swimclub.FOLDER)
        swim_files.remove(".DS_Store")
        session["swimmers"]={}
        for file in swim_files:
            name,*_ = swimclub.read_swim_data(file)
            if name not in session["swimmers"]:
                session["swimmers"][name] = []
            session["swimmers"][name].append(file)

@app.get("/swimmers")
def display_swimmers():
    '''Display the list of swimmers for 
    selection on the web page'''
    populate_data()
    return render_template(
        "select.html",
        title="Select a Swimmer",
        url="/showfiles",
        select_id="swimmer",
        data=sorted(session["swimmers"]),
    )

@app.post("/showfiles")
def display_swimmer_files():
    '''Display the list of files for 
    the selected swimmer'''
    populate_data()
    name=request.form["swimmer"]    
    return render_template(
        "select.html",
        title="Select an event",
        url="/showbarchart",
        select_id="file",
        data=session["swimmers"][name],
        )

@app.post("/showbarchart")
def show_barchart():
    '''Generate and display the bar chart for the selected file'''
    file_id = request.form["file"]
    template_dir = os.path.join(app.root_path, "templates/")
    location = swimclub.produce_bar_chart(file_id, template_dir)
    return render_template(location.split("/")[-1]
    )

if __name__ == "__main__":
    app.run(debug=True)

