#!/usr/bin/env python3
import os

import kaggle


def get_data(outdir: str = "data/raw") -> None:
    """downloads our datasets off kaggle into data"""

    def dl_from_kaggle(dataset: str, datasetname: str, outdir: str) -> None:
        writepath = os.path.join(os.path.abspath(outdir), datasetname)
        os.makedirs(writepath, exist_ok=True)
        kaggle.api.authenticate()  # Note: if failure here, check README for auth directions
        kaggle.api.dataset_download_files(
            dataset, path=writepath, unzip=True, quiet=False
        )

    # delay dataset
    dl_from_kaggle("giovamata/airlinedelaycauses", "delay", outdir)
    dl_from_kaggle("robikscube/flight-delay-dataset-20182022", "btsdelay", outdir)

    # delete the huge, redundant csv files
    dir_name = os.path.abspath(os.path.join(outdir, "btsdelay"))
    files = os.listdir(dir_name)

    for file in files:
        if file.endswith(".csv"):
            os.remove(os.path.join(dir_name, file))


if __name__ == "__main__":
    get_data()
