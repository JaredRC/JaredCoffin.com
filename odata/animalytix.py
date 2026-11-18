import json
from flask import Flask, jsonify, make_response
import mysql.connector
import pandas as pd

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="jaredcoffin.com",
    user="jared",
    password="Surfer@1",
    database="jared"
)

# preparing SQL and cursor object
query = "SELECT * FROM Animalytix"
with db.cursor() as cursor:
    cursor.execute(query)
    cols = [column[0] for column in cursor.description]
    results = cursor.fetchall()

# disconnecting from server
db.close()
df = pd.DataFrame(results, columns=cols)
df['Date'] = df['Date'].astype(str)

@app.route("/test")
def test():
    js = df.to_json(orient='records')
    return js

@app.route('/')
def index():
    data = {
        "@odata.context": "http://jaredcoffin.com/odata/alyx/$metadata",
        "value": [
            {
                "name": "Animalytix",
                "url": "Animalytix"
            }
        ]
    }
    return jsonify(data)

# Minimal OData $metadata endpoint
@app.route("/$metadata", methods=["GET"])
def metadata():
    xml_path = os.path.join(os.path.dirname(__file__), 'animalytics.xml')
    with open(xml_path, 'r', encoding='utf-8') as f:
        metadata_xml = f.read()
    response = make_response(metadata_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

# Minimal OData entity set endpoint
@app.route("/Animalytix", methods=["GET"])
def alyx():
    data = {
  "@odata.context": "http://jaredcoffin.com/odata/alyx/$metadata#Animalytix",
  "value":
      json.loads(df.to_json(orient="records"))
    }
    response = make_response(jsonify(data))
    response.headers["Content-Type"] = "application/json;odata.metadata=minimal"
    response.headers["OData-Version"] = "4.0"
    return response

if __name__ == "__main__":
    app.run()