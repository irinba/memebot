import pandas as pd
from config import DATA_PATH


def load_data() -> pd.DataFrame:
    """
    Загружает данные из all_data.csv, в котором содержатся вся информация о мемах
    (названия, ссылки на страницы, текстовые описания).

    :return: Pandas DataFrame
    """
    return pd.read_csv(DATA_PATH, sep='\t', index_col=0)
