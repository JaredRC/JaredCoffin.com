from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Minimal OData $metadata endpoint
@app.route("/odata/$metadata", methods=["GET"])
def metadata():
    metadata_xml = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0"
    xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="TestService"
        xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EntityType Name="Person">
        <Key><PropertyRef Name="ID"/></Key>
        <Property Name="ID" Type="Edm.Int32"/>
        <Property Name="Name" Type="Edm.String"/>
      </EntityType>
      <EntityContainer Name="Container">
        <EntitySet Name="People" EntityType="TestService.Person"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>"""
    response = make_response(metadata_xml)
    response.headers["Content-Type"] = "application/xml"
    response.headers["OData-Version"] = "4.0"
    return response

# Minimal OData entity set endpoint
@app.route("/odata/Peeple", methods=["GET"])
def people():
    data = {
        "@odata.context": "http://localhost:5000/odata/$metadata#Peeple",
        "value": [
            {"ID": 1, "Name": "Alice"},
            {"ID": 2, "Name": "Bob"}
        ]
    }
    response = make_response(jsonify(data))
    response.headers["Content-Type"] = "application/json;odata.metadata=minimal"
    response.headers["OData-Version"] = "4.0"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)