import os
import pandas as pd
from datetime import datetime

class CombineLogFileData:
    def __init__(self) -> None:
        pass

    def collect_files(self, path):
        file_list = self.get_list_of_files(path)
        
        my_df = pd.DataFrame()
        for my_file in file_list:
            file_path = os.path.join(path, my_file)
            tmp_df = pd.read_csv(file_path, skiprows=6, delimiter="\t", index_col="Zeit")
            my_df = pd.concat([my_df, tmp_df])
        
        my_df.index = pd.to_datetime(my_df.index, unit='s')
        my_df.index = my_df.index.tz_localize('UTC')
        my_df.index = my_df.index.tz_convert('Europe/Berlin')
        my_df = my_df.sort_index()
        my_df = my_df[my_df["DC1 U"].notna()]
        my_df = my_df[my_df["DC2 U"].notna()]
        my_df.to_pickle("pv_data.p")
        my_df.to_csv("py.csv")
        print(my_df.info)

    def get_list_of_files(self, path):
        file_list = os.listdir(path)
        return file_list


if __name__ == "__main__":
    mypath = os.getcwd()
    data_path = os.path.join(mypath, "data")

    my_log = CombineLogFileData()
    my_log.collect_files(data_path)