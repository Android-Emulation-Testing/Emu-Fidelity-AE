import pandas as pd
import ast


def filter_exclusive(df, brand1="emu", brand2="phys", column="type"):
    """get brand1 exclusive dataframe (against brand2)"""
    freq_list = get_freq_list(df, brand1=brand1, brand2=brand2, column=column)
    exclusive_tokens = freq_list.loc[(freq_list[f"ri_{brand1}"] != 0) & (freq_list[f"ri_{brand2}"] == 0)][column].to_list()
    return df.loc[df[column].isin(exclusive_tokens)]


def count(df, column: str) -> pd.DataFrame:
    return df.groupby([column])[column].count().sort_values(ascending=False).reset_index(name='count')


def get_brand_list(df, brand: str, column: str) -> pd.DataFrame:
    if column not in df.columns:
        print("error! failure type identifier not found. Please select a valid column.")
    if brand == "phys":
        df_brand = df[df.device_model != 'virt']
    elif brand == "virt":
        df_brand = df[df.device_model == 'virt']
    else:
        df_brand = df[df.device_brand == brand]

    return count(df_brand, column)


def get_freq_list(df, brand1="phys", brand2="virt", column="type") -> pd.DataFrame:
    """return a dataframe that shows the total number of failure occurrences."""

    brand1_list = get_brand_list(df, brand1, column)
    brand2_list = get_brand_list(df, brand2, column)

    freq_list = brand1_list.merge(brand2_list, how='outer', on=column)
    freq_list = freq_list.fillna(0)  # fill na to avoid exceptions
    freq_list["count"] = freq_list["count_x"] + freq_list["count_y"]
    freq_list = freq_list.rename(columns={'count_x': 'count_' + brand1, 'count_y': 'count_' + brand2})
    order = [column, 'count', 'count_' + brand1, 'count_' + brand2]
    freq_list = freq_list[order]
    return freq_list
