import numpy as np 
import json
import pandas as pd
import os
import math

def get_data_types(nested_list):
    return [[type(element).__name__ for element in sublist] for sublist in nested_list]


def get_ux(ABx, ABy, theta):
    AB_module = math.sqrt(ABx**2 + ABy**2)
    ux0 = ((theta/2) * AB_module) / math.sqrt(1 + (-ABx / ABy)**2)
    ux1 = -ux0
    return [ux0, ux1]

def get_u(ABx, ABy, theta):
    ux = get_ux(ABx, ABy, theta)
    u0 = [
        ux[0],
        (-ABx / ABy) * ux[0]
    ]

    u1 = [
        ux[1],
        (-ABx / ABy) * ux[1]
    ]
    return u0,u1


def get_arrow_points(A,B, theta=0.1):
    A,B = np.array(A), np.array(B)
    AB = B-A
    C = A + (1-theta)*AB
    
    u0, u1 = get_u(AB[0], AB[1], theta)
    u0, u1 = np.array(u0), np.array(u1)
    D = C+u0
    E = C+u1
    
    arrow_points = [
        [A.tolist(), B.tolist()],
        [B.tolist(), D.tolist()],
        [B.tolist(), E.tolist()]
    ]
    return arrow_points

def get_info_dict(info_file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'arrows', 'info', info_file_name)
    with open(file_path, 'r', encoding="utf-8") as file:
        info_dict = json.load(file)
    return info_dict


def get_data_df(info_dict):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'arrows', 'data', info_dict['data_path'])
    data_df = pd.read_csv(data_path)
    return data_df


def make_arrow_feature(coords, color, legend):
    return {
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": coords
        },
        "properties": {
            "type": "arrow",
            "color": color,
            "legend": legend,
            "other": ""
        }
    }


def fill_arrow_features(info_file_name):
    features = []
    info_dict = get_info_dict(info_file_name)
    color = info_dict["color"]
    legend = info_dict["legend"]
    data_df = get_data_df(info_dict)

    for row_idx, row in data_df.iterrows():
        initial_point = [row["initial_lon"], row["initial_lat"]]
        final_point = [row["final_lon"], row["final_lat"]]
        coords = get_arrow_points(initial_point,final_point)
        feature = make_arrow_feature(coords, color, legend)
        features.append(feature)
    
    return features


def feature_collection_base_dict():
    return {
        "type": "FeatureCollection",
        "features": []
    }


def make_arrow_geojson(info_file_name_list):
    geojson = feature_collection_base_dict()
    for info_file_name in info_file_name_list:
        geojson["features"] += fill_arrow_features(info_file_name)

    return geojson
