import pandas as pd


class CsvImporter:
    """Класс для чтения csv"""
    
    def __init__(self, file_obj):
        self.file_obj = file_obj
        self._dataframe = self._read_csv()
        if self._dataframe is None:
            raise FileNotFoundError
        
    def _read_csv(self, sep=","):
        return pd.read_csv(self.file_obj, sep=sep)
    
    @property    
    def df(self):
        return self._dataframe
