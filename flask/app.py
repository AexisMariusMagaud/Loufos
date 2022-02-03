
# Import

import sys
from flask import Flask
from flask import jsonify
from flask.templating import render_template
from flask import request
from TM1py.Services import TM1Service
from TM1py.Utils.Utils import build_pandas_dataframe_from_cellset

tm1_credentials = {
    "address" : "aexfrtma",
    "port" : 8093,
    "user" : "admin",
    "password" : "apple",
    "namespace" : "Logos",
    "ssl" : False
}

# tm1_credentials = {
#    "address" : sys.argv[1],
#    "port" : sys.argv[2],
#    "user" : sys.argv[3],
#    "password" : sys.argv[4],
#    "namespace" : sys.argv[5],
#    "ssl" : False
#}

def returnHTML(data):
    max = 0
    tab_Elements = []

    for thing in data:

        temp = getComplexity(thing[0]['Name'],data,0)
        if temp > max:
            max = temp


        tab_Elements.append([thing[0]['Name'],temp,thing[0]['Weight']])
        
    string =  "<table style='text-align:left'>"
    string += "<thead><tr><th colspan ="+str(max+1)+"> Items </th><th> Weight </th></tr></thead>"

    for row in tab_Elements:
        string += "<tr>"
        

        for k in range(row[1]):
            string += "<td style='border: 1px solid black;border-bottom: none;border-top: none;color:white'> ------ </td>"
        string += "<td colspan = "+str(max-row[1]+1)+" style='border: 1px solid black;'> <label style='color:white'>.</label>" + str(max-row[1]) + " - " + str(row[0]) + "</td><td style='text-align:center'>"+ str(row[2]) + "</td>"
        string += "</tr>\n"

    string += "</table>"
    return string
    
def getComplexity(name,data,sum):
    for thing in data:
        if thing[0]['Name'] == name:
            if thing[0]['Parent'] == None:
                return sum
            else:
                return getComplexity(thing[0]['Parent']['Name'],data,sum+1)
            

    



app = Flask(__name__)

# Live MDX
@app.route("/mdxPageDim")
def mdxPageDim():
    with TM1Service(address=tm1_credentials['address'], port=tm1_credentials['port'], ssl=tm1_credentials['ssl'], user=tm1_credentials['user'], password=tm1_credentials['password']) as tm1:
        data = tm1.dimensions.get_all_names()
    return render_template("/mdxPageDim.html", dims=data)

@app.route("/mdxPageVue")
def mdxPageVue():
    return render_template("/mdxPageVue.html")


@app.route("/refreshMDXdata")
def refreshMDX():
    mdxText = request.args.get('mdx')
    with TM1Service(address=tm1_credentials['address'], port=tm1_credentials['port'], ssl=tm1_credentials['ssl'], user=tm1_credentials['user'], password=tm1_credentials['password']) as tm1:
        dfStatsForServer = ""
        try:
    
            # Requête MDX
            
            dfStatsForServer = build_pandas_dataframe_from_cellset(tm1.cubes.cells.execute_mdx(mdx=mdxText),multiindex=False)
    
            # Chargement du style
            stringReponse = "<table><thead><tr>"
            for j in dfStatsForServer.columns:
                stringReponse += "<th>" + str(j) + "</th>"

            stringReponse += '</tr></thead><tbody>'

            for k in dfStatsForServer.index:
                stringReponse += "<tr>"
                for j in dfStatsForServer.columns:
                    stringReponse += "<td>" + str(dfStatsForServer.loc[k][j]) + "</td>"
                stringReponse += "</tr>"
            stringReponse += "</tbody></table>"
            
            # Return sous forme de tableau HTML 
            
            return stringReponse
        except:
            return "Pas de données correspondante"
     
@app.route("/refreshMDXdim")       
def refreshMDXdim():
    mdxText = "{" + request.args.get('mdx') + "}"
    dimText = request.args.get('dim')
    with TM1Service(address=tm1_credentials['address'], port=tm1_credentials['port'], ssl=tm1_credentials['ssl'], user=tm1_credentials['user'], password=tm1_credentials['password']) as tm1:
        try:
            
            dataMDX = tm1.elements.execute_set_mdx(mdxText)
            return returnHTML(dataMDX)
        except:
            return "Pas de données correspondante"
        
if __name__ == '__main__':
    app.run(debug=True) 