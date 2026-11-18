import json
import os
from flask import Flask, jsonify, make_response
import mysql.connector
import pandas as pd
import time

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="hatetrack.org",
    user="jared",
    password="Surfer@1",
    database="jared"
)

# preparing SQL and cursor object
query = "SELECT ID,Victim,Age,Gender,Race,DateOccured,StreetAddress,City,State,PostalCode"
query += " ,County,AgencyResponsible,Cause_of_Death FROM PoliceViolence"
with db.cursor() as cursor:
    cursor.execute(query)
    cols = [column[0] for column in cursor.description]
    results = cursor.fetchall()

# disconnecting from server
db.close()
df = pd.DataFrame(results, columns=cols)
df['Age'] = df['Age'].astype('int')
df['DateOccured'] = df['DateOccured'].astype(str)

@app.route("/test")
def test():
    js = df.to_json(orient='records')
    return js

@app.route('/')
def index():
    version = int(time.time())
    data = {
        "@odata.context": f"http://hatetrack.org/odata/police/$metadata?v={version}",
        "value": [
            {
                "name": "PoliceViolence",
                "url": f"PoliceViolence?v={version}"
            }
        ]
    }
    return jsonify(data)

# Minimal OData $metadata endpoint
@app.route("/$metadata", methods=["GET"])
def metadata():
    xml_path = os.path.join(os.path.dirname(__file__), 'police.xml')
    with open(xml_path, 'r', encoding='utf-8') as f:
        metadata_xml = f.read()
    response = make_response(metadata_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

# Minimal OData entity set endpoint
@app.route("/PoliceViolence", methods=["GET"])
def police():
    data = {
  "@odata.context": "http://hatetrack.org/odata/police/$metadata#PoliceViolence",
  "value":
      json.loads(df.to_json(orient="records"))
    }
    response = make_response(jsonify(data))
    response.headers["Content-Type"] = "application/json;odata.metadata=minimal"
    response.headers["OData-Version"] = "4.0"
    return response

if __name__ == "__main__":
    app.run()