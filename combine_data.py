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

        # Delete unnecessary columns:    
        del_cols = ["DC1 T", "DC1 S", "DC2 T", "DC2 S", "DC3 T", "DC3 S",
                    "Ain1", "Ain2", "Ain3", "Ain4", "Err", "FC I", "AC S",
                    "ENS S", "ENS Err", "HC1 P", "SOC H", "BAT Te", "BAT Cy",
                    "KB S", "total E", "OWN E", "HOME E", "Iso R", "Ereignis",
                    "SH2 P", "SH3 P", "SC1 P", "SC2 P", "SC3 P"]

        my_df = my_df.drop(columns=del_cols, axis=1)

        # Set datetime index:
        my_df.index = pd.to_datetime(my_df.index, unit='s')
        my_df.index = my_df.index.tz_localize('UTC')
        my_df.index = my_df.index.tz_convert('Europe/Berlin')
        my_df = my_df.sort_index()
        my_df = my_df[my_df["DC1 U"].notna()]
        my_df = my_df[my_df["DC2 U"].notna()]
        # transder mA to A
        my_df["DC1 I"] = my_df["DC1 I"] / 1000.0
        my_df["DC2 I"] = my_df["DC2 I"] / 1000.0
        #my_df["DC3 I"] = my_df["DC3 I"] / 1000.0
        my_df["AC1 I"] = my_df["AC1 I"] / 1000.0
        my_df["AC2 I"] = my_df["AC2 I"] / 1000.0
        my_df["AC3 I"] = my_df["AC3 I"] / 1000.0

        # Compute timedelta between the rows
        my_df['dT'] = my_df.index.to_series().diff().astype('timedelta64[s]')

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