import pandas as pd


class DataframeImporter:
    """Класс импорта pd.DataFrame в бд"""
    
    def __init__(self, dataframe, models_map, main_model):
        self.dataframe = dataframe
        self.models_map = models_map
        self.main_model = main_model
    
    def _get_cols_from_index(self, index=1):
        return self.dataframe.iloc[:, 1:]

    def get_col_unique_values(self, col_name=None, col_index=None):
        if col_name:
            return self.df[col_name].dropna().unique()
        elif col_index:
            return self.df.iloc[:, col_index].dropna().unique()
        return self.df

    @property
    def df(self):
        normal_df = self._get_cols_from_index()
        return normal_df

    
    @property
    def secondary_tables_data(self):
        out_dict = {}
        for col_name, model in self.models_map.items(): 
            col_unique_values = self.get_col_unique_values(col_name=col_name).tolist()
            out_dict[model.__tablename__] = col_unique_values
        return out_dict

        