from flask import Flask, render_template, jsonify, request
from .database.list_json import get_info_list
from .database.polygon_geojson import make_poly_geojson
from .database.arrow_geojson import make_arrow_geojson
from .database.point_geojson import make_point_geojson

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("map.html")

@app.route("/base-select-info")
def base_select_info():
    return jsonify(get_info_list("polygons/info"))

@app.route("/point-select-info")
def point_select_info():
    return jsonify(get_info_list("points/info"))

@app.route("/arrow-select-info")
def arrow_select_info():
    return jsonify(get_info_list("arrows/info"))

@app.route("/polygon-geojson")
def polygon_geojson():
    # url: source.com/polygon-geojson?value=someValue
    query = request.args.to_dict(flat=False)
    value = query["value"]
    info_file_name = value[0] + ".json"
    poly_geojson = make_poly_geojson(info_file_name)
    return jsonify(poly_geojson)

@app.route("/arrow-geojson")
def arrow_geojson():
    # url: source.com/arrow-geojson?value=someValue&value=anotherValue
    query = request.args.to_dict(flat=False)
    values = query["value"]
    info_file_name_list = [val + ".json" for val in values]
    arrow_geojson = make_arrow_geojson(info_file_name_list)
    return jsonify(arrow_geojson)

@app.route("/point-geojson")
def point_geojson():
    # url: source.com/point-geojson?value=someValue&value=anotherValue
    query = request.args.to_dict(flat=False)
    values = query["value"]
    info_file_name_list = [val + ".json" for val in values]
    point_geojson = make_point_geojson(info_file_name_list)
    return jsonify(point_geojson)

@app.route("/data-sources")
def data_sources():
    return render_template("data_sources.html")