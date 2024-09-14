import os
from typing import List
from datetime import datetime
import json

import xarray as xr
from xarray.core.dataset import Dataset
import copernicusmarine

from . import features
# from __init__ import features

from backend.api.service.logging.logger import Logger


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
        self.logger = Logger()

        with open(creds_path) as f:
            creds = json.load(f)
        self.username = creds["username"]
        self.password = creds["password"]

        copernicusmarine.login(username=self.username, password=self.password, overwrite_configuration_file=True)
        self.logger.message(__file__, "Logged in to Copernicus Successfully")

        self.update()
        self.data = self.load_data()

    def _get_current_deets(self):
        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        return year, month, day

    def _format_filename(self):
        year, month, day = self._get_current_deets()
        filename = self.filename_format.format(year=year, month=month, day=day)
        return filename

    def _delete_old_files(self):
        files = self.get_files()
        if not files: return
        files.remove(max(files))
        for file in files:
            self.logger.message(__file__, f"Deleting Dataset: {file}")
            os.remove(os.path.join(self.dataset_path, file))

    def get_files(self) -> List[str]:
        files = os.listdir(self.dataset_path)
        return [x for x in files if x.endswith(".nc")]

    def load_data(self, _updated=False) -> Dataset:
        if not self.data or _updated:  # load the data afresh if newly updated, or first time loading.
            files = self.get_files()

            latest = max(files)  # latest dataset will be lexicographically largest
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
        # latest_name = "cmems_2024-09-13.nc"

        if latest_name not in self.get_files():
            self._download_subset()
            self.load_data(_updated=True)
        # todo: implement daily updates
        self.logger.message(__file__, "Downloaded and loaded!")
        # delete every other dataset
        self._delete_old_files()
        self.logger.message(__file__, "Old ones deleted.!")

