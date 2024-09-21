import pandas as pd
import unicodedata
import os

def normalize_mun_names(text):
    # Normalize the text to decompose characters with accents into their base characters
    normalized_text = unicodedata.normalize('NFD', text)
    # Filter out the diacritical marks (combining characters)
    normalized_text = ''.join(char for char in normalized_text if unicodedata.category(char) != 'Mn')
    normalized_text = normalized_text.lower()
    normalized_text = ''.join([char for char in normalized_text if char.isalpha()])
    return normalized_text



def get_mun_coords_df():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mun_coords_df_path = os.path.join(script_dir, "municipios_coords.csv")
    mun_coords_df = pd.read_csv(mun_coords_df_path)
    mun_coords_df["norm_name"] = mun_coords_df["nome"].apply(normalize_mun_names) 
    return mun_coords_df


def get_initial_points_df(storage_units, prod_units):
    points_df = {"municipio": [], "Período Instalação":[], "legend": [], "file_name": []}
    for idx, row in storage_units.iterrows():
        first_column_value  = eval(row.tolist()[0])
        try:
            ano_instalacao = first_column_value[1]
        except IndexError:
            ano_instalacao = 1

        points_df["municipio"].append(first_column_value[0])
        points_df["legend"].append("Unidade de Armazenamento")
        points_df["file_name"].append("S_units")
        points_df["Período Instalação"].append(ano_instalacao)

    
    for idx, row in prod_units.iterrows():
        first_column_value  = eval(row.tolist()[0])
        try:
            ano_instalacao = first_column_value[2]
        except IndexError:
            ano_instalacao = 1

        points_df["municipio"].append(first_column_value[0])
        points_df["legend"].append(f"Unidade de Produção ({first_column_value[1]})")
        points_df["file_name"].append(f"P_units_{first_column_value[1]}")
        points_df["Período Instalação"].append(ano_instalacao)
    
    points_df = pd.DataFrame(points_df)
    points_df = points_df.groupby(by="municipio").min()
    points_df = points_df.reset_index()
    return points_df



def add_capacities(points_df_row, output_df):
    mun_name = points_df_row["municipio"]
    is_storage_unit = points_df_row["legend"] == "Unidade de Armazenamento"
    
    if is_storage_unit:
        capac_col_name = "ESTOQUE_CAPAC"
        product_idx = 1
    else: # is_prod_unit
        capac_col_name = "MPZ_CAPAC"
        product_idx = 2

    capac_df = output_df.loc[output_df[capac_col_name]>0]
    points_df_row["Capacidade"] = ""

    for idx, row in capac_df.iterrows():
        first_column_value  = eval(row.tolist()[0])

        if first_column_value[0] == mun_name:
            capac = row[capac_col_name]
            capac_str = "{:.2f}".format(capac)
            capac_str = f"{capac_str} ton {first_column_value[product_idx]}/ano"
            points_df_row["Capacidade"] = capac_str
            break
    
    return points_df_row






def add_point_coords(points_df_row, mun_coords_df):
    mun_name = points_df_row["municipio"]
    norm_mun_name = normalize_mun_names(mun_name)
    mun_info = mun_coords_df.loc[mun_coords_df["norm_name"] == norm_mun_name]
    lat, lon = mun_info.iloc[0][["latitude", "longitude"]]
    points_df_row["lat"] = lat
    points_df_row["lon"] = lon
    return points_df_row



def get_colorless_points(output_df):
    mun_coords_df = get_mun_coords_df()

    prod_units = output_df[(output_df["INSTALAR_P_Z"] > 0.99) & (output_df["INSTALAR_P_Z"] < 1.01)]
    storage_units = output_df[(output_df["INSTALAR_S"] > 0.99) & (output_df["INSTALAR_S"] < 1.01)]

    points_df = get_initial_points_df(storage_units, prod_units)
    points_df = points_df.apply(lambda row: add_point_coords(row, mun_coords_df), axis=1)
    points_df = points_df.apply(lambda row: add_capacities(row, output_df), axis=1)

    colorless_points = {}
    for file_name in points_df["file_name"].unique():
        data = points_df.loc[points_df["file_name"] == file_name]
        info = {
            "data_path": f"{file_name}.csv",
            "legend": data["legend"][0],
            "color": ""
        }
        data = data[["lon", "lat", "Período Instalação", "Capacidade"]]
        colorless_points[file_name] = [data, info]

    return colorless_points
    


def select_non_null_arrows(output_df):
    cond_1 = output_df["MP_O_PARA_P"].apply(lambda x: round(x)) > 0
    cond_2 = output_df["PRODUTO_P_PARA_S"].apply(lambda x: round(x)) > 0
    cond_3 = output_df["PRODUTO_P_PARA_M"].apply(lambda x: round(x)) > 0
    cond_4 = output_df["PRODUTO_S_PARA_S"].apply(lambda x: round(x)) > 0
    cond_5 = output_df["PRODUTO_S_PARA_M"].apply(lambda x: round(x)) > 0
    combined_conds = cond_1 | cond_2 | cond_3 | cond_4 | cond_5

    arrows = output_df.loc[combined_conds].iloc[:, 0]  # first column
    return arrows


def add_coords(position, mun_coords_df, row):
    # position must be "initial" or "final"
    mun = row[f"{position}_mun"]
    norm_mun_name = normalize_mun_names(mun)

    mun_info = mun_coords_df.loc[mun_coords_df["norm_name"] == norm_mun_name]
    lat, lon = mun_info.iloc[0][["latitude", "longitude"]]
    row[f"{position}_lat"] = lat
    row[f"{position}_lon"] = lon
    return row



def get_arrows_df(output_df):
    output_df = output_df.copy()
    output_df = output_df.fillna(value=0)

    arrows = select_non_null_arrows(output_df)
    arrows = arrows.apply(lambda x: eval(x)[:3])  # ignore year
    arrows = arrows.drop_duplicates()
    arrows = [list(arrow) for arrow in arrows]

    arrows_df_cols = ["initial_mun", "final_mun", "product"]
    arrows_df = pd.DataFrame(arrows, columns=arrows_df_cols)
    arrows_df = arrows_df.loc[arrows_df["initial_mun"] != arrows_df["final_mun"]]

    mun_coords_df = get_mun_coords_df()
    arrows_df = arrows_df.apply(lambda row: add_coords("initial", mun_coords_df, row) , axis=1)
    arrows_df = arrows_df.apply(lambda row: add_coords("final", mun_coords_df, row) , axis=1)
    return arrows_df



def get_colorless_arrows(output_df):
    arrows_df = get_arrows_df(output_df)

    colorless_arrows = {}
    for product in arrows_df["product"].unique():
        data_cols = ["initial_lat", "initial_lon", "final_lat", "final_lon"]
        data = arrows_df.loc[arrows_df["product"] == product]
        data = data[data_cols]

        info = {
            "data_path": f"{product}.csv",
            "legend": product.capitalize(),
            "color": ""
        }

        colorless_arrows[product] = [data, info]
    
    return colorless_arrows











    

    






