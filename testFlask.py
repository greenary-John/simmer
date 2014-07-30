from flask import Flask
from flask import request 

import json

app = Flask(__name__)

@app.route("/")
def simmerWSP():
    annSetChoice = request.values.get('annSet')
    evCodesChoice = request.values.getlist('ecode')
    searchType  = request.values.get('qtype')
    searchInput  = request.values.getlist('qid')
    namespaceChoice = request.values.get('nspace')
    method = request.values.get('method')
    length = request.values.get('length')
    return json.dumps([annSetChoice,str(evCodesChoice),searchType,searchInput,namespaceChoice,method,length])

if __name__ == "__main__":
    app.run(debug=True)
