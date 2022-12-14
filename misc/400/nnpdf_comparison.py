#!/usr/bin/env python3
"""
Compare the fktables computed with pineko with fktables from NNPDF

This script uses validphys and so the comparison is made at the dataset level
"""
import argparse
import sys
from pathlib import Path
from yaml import safe_load

import numpy as np
import pandas as pd

from validphys.api import API
from validphys.convolution import central_predictions

import lhapdf, NNPDF

lhapdf.setVerbosity(0)
NNPDF.SetVerbosity(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("new_th", type=int, help="New theory number")
    parser.add_argument("datasets", nargs="*", help="Datasets to compare")
    parser.add_argument(
        "-r", "--runcard", type=Path, help="Path to a NNPDF runcard to read the datasets from"
    )
    parser.add_argument("--ref_th", default=400, type=int, help="Reference theory")
    parser.add_argument("--pdf", default="NNPDF40_nnlo_as_01180")
    parser.add_argument(
        "--acc",
        default=1e-16,
        help="Don't print anything for which the accuracy is better than this",
        type=float,
    )
    parser.add_argument("-o", "--output", help="Output folder to write the CSV files of the comparisons as output/dataset.csv")
    args = parser.parse_args()

    if args.runcard is None and not args.datasets:
        print(
            "I need either a list of datasets to compare or a runcard to read the datasets from, you gave me nothing!"
        )
        sys.exit(-1)

    datasets = [{"dataset": i} for i in args.datasets]

    if args.runcard is not None:
        datasets += safe_load(args.runcard.read_text())["dataset_inputs"]

    # Read the comparison PDF
    pdf = API.pdf(pdf=args.pdf)

    # Get a reasonable fit for the cuts
    fit = "NNPDF40_nnlo_as_01180_1000"

    for dataset in datasets:
        dsname = dataset["dataset"]

        if "JET" in dsname:
            continue

        # Read the reference theory
        ds_ref = API.dataset(dataset_input=dataset, theoryid=args.ref_th, use_cuts="fromfit", fit=fit)
        ds_new = API.dataset(dataset_input=dataset, theoryid=args.new_th, use_cuts="fromfit", fit=fit)

        res_ref = central_predictions(ds_ref, pdf)
        res_new = central_predictions(ds_new, pdf)
        ratio = res_ref / res_new

        # Print a comparison
        comparison = pd.concat([res_ref, res_new, ratio], axis=1, keys=["Reference", "New", "ratio"])
        if args.output is not None:
            comparison.to_csv(f"{args.output}/{dsname}.csv")

        if np.allclose(res_new, res_ref, rtol=args.acc):
            print(f"Perfect agreement for {dsname}")
        else:
            print(f"Problems for {dsname}")
            print(comparison)
