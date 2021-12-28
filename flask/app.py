
# Import

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
                    stringReponse += "<td '>" + str(dfStatsForServer.loc[k][j]) + "</td>"
                stringReponse += "</tr>"
            stringReponse += "</tbody></table>"
            
            # Return sous forme de tableau HTML 
            
            return stringReponse
        except:
            return "Pas de données correspondante"
     
@app.route("/refreshMDXdim")       
def refreshMDXdim():
    mdxText = request.args.get('mdx')
    dimText = request.args.get('dim')
    with TM1Service(address=tm1_credentials['address'], port=tm1_credentials['port'], ssl=tm1_credentials['ssl'], user=tm1_credentials['user'], password=tm1_credentials['password']) as tm1:
        try:
            dfStatsForServer = ""
            dfStatsForServer = tm1.dimensions.execute_mdx(dimText,mdxText)
            # Chargement du style
            return '<br>'.join(dfStatsForServer)
        except:
            return "Pas de données correspondante"
        
if __name__ == '__main__':
    app.run(debug=True) 