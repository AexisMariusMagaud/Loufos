
from re import template
from flask import Flask
from flask import jsonify
from flask.templating import render_template
import pyodbc
from flask import request

import TM1py
from TM1py.Services import TM1Service
from TM1py.Utils.Utils import build_pandas_dataframe_from_cellset

g_server = 'aexfrtma.aexis.com'
g_database = 'logos'
g_username = 'sa'
g_password = 'Password1'

tm1_credentials = {
    "address" : "aexfrtma",
    "port" : 8093,
    "user" : "admin",
    "password" : "",
    "namespace" : "Logos",
    "ssl" : False
}


def getCursor():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+g_server+';DATABASE='+g_database+';UID='+g_username+';PWD='+g_password)
    cursor = cnxn.cursor()
    return cursor


app = Flask(__name__)

# Live MDX

@app.route("/liveMDX")
def liveMDX():
    return render_template("/liveMdx.html")

@app.route("/liveMdx/refreshMDX")
def refreshMDX():
    mdxText = request.args.get('mdx')
    with TM1Service(address=tm1_credentials['address'], port=tm1_credentials['port'], ssl=tm1_credentials['ssl'], user=tm1_credentials['user'], password=tm1_credentials['password']) as tm1:
        dfStatsForServer = ""
        try:
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
            return stringReponse
        except:
            return "Pas de données correspondante"
     
@app.route("/liveMdx/refreshMDXdim")       
def refreshMDXdim():
    mdxText = request.args.get('mdx')
    with TM1Service(address=tm1_credentials['address'], port=tm1_credentials['port'], ssl=tm1_credentials['ssl'], user=tm1_credentials['user'], password=tm1_credentials['password']) as tm1:
        dfStatsForServer = ""
        dfStatsForServer = tm1.dimensions.execute_mdx("Client_facture",mdxText)
        # Chargement du style
        return '<br>'.join(dfStatsForServer)    
if __name__ == '__main__':
    app.run(debug=True) 