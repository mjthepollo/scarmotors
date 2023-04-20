import pandas as pd

END = 56
DAY_CAME_IN = 2


def load_data(file_name, sheet_name):
    df = pd.read_excel(
        file_name, sheet_name=sheet_name, engine="openpyxl", header=5, index_col=2
    )
    return df


def get_effective_row_numbers(df):
    days_came_in = df.iloc[:, DAY_CAME_IN]
    for i, day_came_in in enumerate(days_came_in):
        if pd.isnull(day_came_in):
            return i


def get_effective_data_frame(file_name, sheet_name):
    original_df = load_data(file_name, sheet_name)
    effective_row_numbers = get_effective_row_numbers(original_df)
    return original_df.iloc[:effective_row_numbers, :END]


# -------------pandas utility finish---------------#
