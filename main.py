import pandas as pd

from server.app import app
from outputtransformer.delete_runs import delete_previous_runs
from outputtransformer.output_transformer import get_colorless_points, get_colorless_arrows
from outputtransformer.color_and_save import color_info,save_colored_dict

def load_output_data(output_df_path):
    points_to_keep = ["centros_operativos.json","depositos.json","capitais_brasileiras.json","portos.json"]
    delete_previous_runs(points_to_keep)
    output_df = pd.read_excel(output_df_path)
    colorless_points = get_colorless_points(output_df)
    colorless_arrows = get_colorless_arrows(output_df)

    colored_points = color_info(colorless_points)
    colored_arrows = color_info(colorless_arrows)

    save_colored_dict(colored_points, points=True)
    save_colored_dict(colored_arrows, arrows=True)

load_output_data("model_output.xlsx")
app.run(debug=True)