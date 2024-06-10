import json
import pandas as pd

def get_info_dict(info_file_name):
    file_path = f"points/info/{info_file_name}"
	with open(file_path, 'r') as file:
        info_dict = json.load(file)
    return info_dict


def get_data_df(info_dict):
    data_path = f"points/data/{info_dict['data_path']}"
    data_df = pd.read_csv(data_path)
    return data_df


def create_other_entry(row, other_cols):
    # col = column
    other_html = ""
    for col in other_cols:
        other_html += f"<p>{col}: {row[col]}</p>"
    
    row["other"] = other_html
    return row


def feature_collection_base_dict():
    return {
        "type": "FeatureCollection",
        "features": []
    }


def make_point_feature(lat, lon, color, other, legend):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "properties": {
            "color": color,
            "legend": legend,
            "other": other
        }
    }


def fill_point_features(info_file_name):
    point_features = []

    info_dict = get_info_dict(info_file_name)
    data_df = get_data_df(info_dict)

    mandatory_cols = ["lat", "lon"]
    other_cols = [col for col in df.columns if col not in mandatory_cols]
    data_df = data_df.apply(lambda row: create_other_entry(row, other_cols), axis=1)
    
    color = info_dict["color"]
    legend = info_dict["legend"]

    for row_idx, row in data_df.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        other = row["other"]
        point_features.append(
            make_point_feature(lat, lon, color, other, legend)
        )
    
    return point_features


def make_point_geojson(info_file_name_list):
    geojson = feature_collection_base_dict()

    for info_file_name in info_file_name_list:
        point_features = fill_point_features(info_file_name)
        geojson["features"] += point_features

    return geojson