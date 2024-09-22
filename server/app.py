import os
import pandas as pd

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

@app.route("/vpl-demanda-rotas")
def vpl_demanda_rotas():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    file_path = os.path.join(parent_dir, "model_output.xlsx")

    if not os.path.exists(file_path):
        return jsonify({})       
    else:
        output_df = pd.read_excel(file_path)
        vpl = output_df.loc[output_df["VPL"] > 0]
        vpl = vpl["VPL"].tolist()[0]

        demanda = output_df.loc[output_df["DEMANDA_TOTAL_ATENDIDA"] > 0]
        demanda = demanda["DEMANDA_TOTAL_ATENDIDA"].tolist()[0]

        rotas = []
        storage_units = output_df[(output_df["INSTALAR_P_Z"] > 0.99) & (output_df["INSTALAR_P_Z"] < 1.01)]
        for idx, row in storage_units.iterrows():
            first_column_value  = eval(row.tolist()[0])
            rota = first_column_value[1]
            if rota not in rotas:
                rotas.append(rota)
        
        print(rotas)
        rotas_dict = {
            "desidratacao": "Desidratação",
            "hvo": "HVO",
            "gaseificacao": "Gaseificação"
        }

        rotas = [rotas_dict[rota] if rota in rotas_dict.keys() else rota for rota in rotas]
        rotas = ", ".join(rotas)

        result = {
            "Rotas utilizadas": rotas,
            "Demanda atendida (ton)": "{:,.2f}".format(demanda),
            "VPL (R$)": "{:,.2f}".format(vpl)
        }
        return jsonify(result)





@app.route("/data-sources")
def data_sources():
    return render_template("data_sources.html")
