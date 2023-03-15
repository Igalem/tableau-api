from flask import Flask, flash, render_template, request, flash
import sys
sys.path.append(".")
from api.tabcmd import tableau_api

filepath='/Users/igale/Downloads'

app=Flask(__name__)
app.secret_key="xxxxxxxxx"
ds_id=''

@app.route("/")
def index():
    #flash("Search for:")
    return render_template("index.html")

@app.route("/search", methods=["POST", "GET"])
def search():
    print('x')
    tabcmd=tableau_api(server='xxxxx', 
                    user='xxxx', 
                    token = 'xxxxxxx')
    datasources=tabcmd.datasource_list(str(request.form['search_input']))
    results=len(datasources)
    ds_id=str(request.form['ds_id_input'])
    if len(ds_id)==0:
        flash(str(results) +' results for "' + str(request.form['search_input']) + '":')
    for ds in datasources:
        flash(str(ds[0]) + " | " + str(ds[1]))
       
    if len(ds_id) >0:
        dnld_msg=tabcmd.datasource_download_id_no_extract(ds_id=ds_id,filepath=filepath)
        flash(str(dnld_msg))
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True) ## run the application in debug mode (refresh code and page)

#