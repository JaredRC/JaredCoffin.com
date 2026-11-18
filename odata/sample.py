from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "@odata.context": "http://jaredcoffin.com/odata/sample/$metadata",
        "value": [
            {
                "name": "People",
                "url": "People"
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
      <EntityType Name="Person" OpenType="true">
        <Key>
          <PropertyRef Name="ID"/>
        </Key>
        <Property Name="ID" Type="Edm.Int32" Nullable="false"/>
        <Property Name="Name" Type="Edm.String"/>
        <Property Name="Age" Type="Edm.Int32"/>
      </EntityType>
      <EntityContainer Name="Container">
        <EntitySet Name="People" EntityType="JaredService.Person"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>"""
    response = make_response(metadata_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

# Minimal OData entity set endpoint
@app.route("/People", methods=["GET"])
def people():
    data = {
  "@odata.context": "http://jaredcoffin.com/odata/sample/$metadata#People",
  "value": [
    {
      "ID": 1,
      "Name": "Alice",
      "Age": 30
    },
    {
      "ID": 2,
      "Name": "Bob",
      "Age": 25
    }
  ]
}
    response = make_response(jsonify(data))
    response.headers["Content-Type"] = "application/json;odata.metadata=minimal"
    response.headers["OData-Version"] = "4.0"
    return response

if __name__ == "__main__":
    app.run()