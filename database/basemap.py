import sqlite3
import json
import pandas as pd

def make_geojson(production_lot_id):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    query_str = """
    SELECT region.id, region.name, region.geometry, region.geometry_type, lot_entry.quantity_produced
    FROM lot_entry
    INNER JOIN region ON lot_entry.region_id = region.id
    WHERE lot_entry.lot_id = ?
    """
    result = cursor.execute(query_str, [production_lot_id])

    for feature_info in result:
        region_id, name, geometry, geometry_type, quantity_produced = feature_info
        feature = {
            "type": "Feature",
            "properties":{
                "name": name,
                "quantity": quantity_produced
            },
            "geometry": {
                "type": geometry_type,
                "coordinates": json.loads(geometry)
            }

        }

        geojson["features"].append(feature)


    connection.close()
    return geojson