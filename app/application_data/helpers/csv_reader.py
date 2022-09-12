import pandas as pd


class CsvImporter:
    """Класс для чтения csv"""
    
    def __init__(self, file_obj, models_map, main_model):
        self.file_obj = file_obj
        self.models_map = models_map
        self.main_model = main_model
        
        self._dataframe = self._read_csv()
        if self._dataframe is None:
            raise FileNotFoundError
        
    def _read_csv(self, sep=","):
        return pd.read_csv(self.file_obj, sep=sep)
    
    def _get_cols_from_index(self, index=1):
        return self._dataframe.iloc[:, 1:]

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
