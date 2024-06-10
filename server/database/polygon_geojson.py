import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def get_info_dict(info_file_name):
    file_path = f"polygons/info/{info_file_name}"
    with open(file_path, 'r') as file:
        info_dict = json.load(file)
    return info_dict


def get_data_df(info_dict):
    data_path = f"polygons/data/{info_dict['data_path']}"
    data_df = pd.read_csv(data_path)
    return data_df


def get_geojson_gdf(info_dict):
    geojson_path = f"polygons/geojson/{info_dict['region_geojson']}"
    geojson_gdf = gpd.read_file(geojson_path)
    return geojson_gdf


def get_metadata(info_dict):
    # should be: {"center_lat": lat, "center_lon": lon, "zoom_level": zoom...}
    geojson_path = f"polygons/geojson/{info_dict['region_geojson']}"
    with open(geojson_path, 'r') as file:
        metadata = json.load(file)["metadata"]
    return metadata


def create_other_entry(row, other_cols):
    # col = column
    other_html = ""
    for col in other_cols:
        other_html += f"<p>{col}: {row[col]}</p>"
    
    row["other"] = other_html
    return row


def make_poly_geojson(info_file_name):
    info_dict = get_info_dict(info_file_name)
    data_df = get_data_df(info_dict)
    geojson_gdf = get_geojson_gdf(info_dict)
    metadata = get_metadata(info_dict)
    gdf = geojson_gdf.merge(data_df, on="region_id", how="inner")

    all_cols = gdf.columns
    mandatory_cols = ["region_id", "value", gdf.geometry.name]
    other_cols = [col for col in all_cols if col not in mandatory_cols]
    gdf = gdf.apply(lambda row: create_other_entry(row, other_cols), axis=1)
    
    gdf = gdf.assign(valueTitle=info_dict["value_title"])
    gdf = gdf.assign(valueUnit=info_dict["value_unit"])

    gdf = gdf[["value", "valueTitle", "valueUnit", "other", gdf.geometry.name]]
    geojson = gdf.to_json()
    geojson = json.loads(geojson)
    geojson["metadata"] = metadata
    return geojson

