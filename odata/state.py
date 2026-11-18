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
query = "SELECT * FROM StateRegion"
with db.cursor() as cursor:
    cursor.execute(query)
    cols = [column[0] for column in cursor.description]
    results = cursor.fetchall()

# disconnecting from server
db.close()
df = pd.DataFrame(results, columns=cols)

@app.route('/')
def index():
    data = {
        "@odata.context": "http://jaredcoffin.com/odata/state/$metadata",
        "value": [
            {
                "name": "StateRegion",
                "url": "StateRegion"
            }
        ]
    }
    return jsonify(data)

# Minimal OData $metadata endpoint
@app.route("/$metadata", methods=["GET"])
def metadata():
    metadata_xml = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0"
           xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="JaredService" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EntityType Name="StateRegion" OpenType="true">
        <Key>
          <PropertyRef Name="StateCode"/>
        </Key>
        <Property Name="StateCode" Type="Edm.String" Nullable="false"/>
        <Property Name="State" Type="Edm.String"/>
        <Property Name="Region" Type="Edm.String" Nullable="false"/>
        <Property Name="Zone" Type="Edm.String"/>
      </EntityType>
      <EntityContainer Name="Container">
        <EntitySet Name="StateRegion" EntityType="JaredService.StateRegion"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>"""
    response = make_response(metadata_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

# Minimal OData entity set endpoint
@app.route("/StateRegion", methods=["GET"])
def police():
    data = {
  "@odata.context": "http://jaredcoffin.com/odata/state/$metadata#StateRegion",
  "value":
      json.loads(df.to_json(orient="records"))
    }
    response = make_response(jsonify(data))
    response.headers["Content-Type"] = "application/json;odata.metadata=minimal"
    response.headers["OData-Version"] = "4.0"
    return response

if __name__ == "__main__":
    app.run()