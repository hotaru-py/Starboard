import asyncio
import os
from typing import List
from datetime import datetime
import json

import xarray as xr
from xarray.core.dataset import Dataset
import copernicusmarine

from . import features


# backend/api/service/dataset/creds.json file format
# {
#     "username": "username",
#     "password": "password"
# }


class DatasetLoader:
    _instance = None  # singleton class

    def __new__(cls, *args, **kwargs):
        if DatasetLoader._instance is None:
            DatasetLoader._instance = object.__new__(cls)
            DatasetLoader._instance.__init__(*args, **kwargs)

        return DatasetLoader._instance

    def __init__(self):
        self.data = None
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.dataset_path = os.path.join(self.current_path, "data")
        self.filename_format = "cmems_{year}-{month:02d}-{day:02d}.nc"
        creds_path = os.path.join(self.current_path, "creds.json")

        with open(creds_path) as f:
            creds = json.load(f)
        self.username = creds["username"]
        self.password = creds["password"]

        self.data = self.load_data()
        self.update()
        copernicusmarine.login(username=self.username, password=self.password, overwrite_configuration_file=True)
        print("Logged in Successfully")

    def _get_current_deets(self):
        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        return (year, month, day)

    def _format_filename(self):
        year, month, day = self._get_current_deets()
        filename = self.filename_format.format(year=year, month=month, day=day)
        return filename

    def get_files(self) -> List[str]:
        files = os.listdir(self.dataset_path)
        return [x for x in files if x.endswith(".nc")]

    def load_data(self, _updated=False) -> Dataset:
        if not self.data or _updated:  # load the data afresh if newly updated, or first time loading.
            files = self.get_files()
            latest = max(files)  # latest dataset will be lexicographically largest
            print(latest)
            latest_path = os.path.join(self.dataset_path, latest)
            self.data = xr.open_dataset(latest_path)

        return self.data

    def _download_subset(self):
        year, month, day = self._get_current_deets()
        filename = self._format_filename()

        copernicusmarine.subset(
            dataset_id="cmems_mod_glo_wav_anfc_0.083deg_PT3H-i",
            variables=[x for x in features],
            minimum_longitude=-180,
            maximum_longitude=179.91666666666666,
            minimum_latitude=-80,
            maximum_latitude=90,
            start_datetime=f"{year:02d}-{month:02d}-{day:02d}T00:00:00",
            end_datetime=f"{year:02d}-{month:02d}-{day:02d}T00:00:00",
            output_filename=filename,
            output_directory=self.dataset_path,
            force_download=True
        )

    def update(self) -> None:
        latest_name = self._format_filename()

        if latest_name in self.get_files():
            # if "cmems_2024-09-13.nc" in self.get_files():  # we have placeholder for now
            return
        else:
            self._download_subset()
            self.load_data(_updated=True)
        # todo: implement daily updates


if __name__ == '__main__':
    d = DatasetLoader()
    d.update()
