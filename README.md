# Artifact for MobiCom'23: Virtual Device Farms for Mobile App Testing at Scale: A Pursuit for Fidelity, Efficiency, and Accessibility

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
<a href="https://colab.research.google.com/drive/19DYtr3yrJs6aKrXXyKWrBbMsCEvw46qw?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="google colab logo"></a>

## Overview

This repository contains the anonymized failure data collected from our physical and device farms over a three-month period. The failure data involves 5,918 physical devices as well as 5,918 virtualized devices running on ARM commodity servers.

For more details, please visit our website ([Android-Emulation-Testing.github.io](https://android-emulation-testing.github.io/)) or read our paper:
* Virtual Device Farms for Mobile App Testing at Scale: A Pursuit for Fidelity, Efficiency, and Accessibility

## Data Format

We present the failure data we collected in the `data.csv` spreadsheet (which you can obtain after running the evaluation script, or manually decompressing `data.zip`). 

Each row represents a single failure scene, and detailed information (i.e. call stacks, device information) about the scenes is provided, in the format described in the table below.

Part of our data is anonymized due to the request of our legal department.

| Column | Description | Example |
| ------ | ----------- | ------- |
| type | A number that labels failure type. Failures that belong to the same type have the same number. | 1 |
| error | The triggered exception/signal of the failure | java.lang.NullPointerException |
| reason | The descriptive message printed after the error | must not be null |
| stack_frame | The call stack of the failure | [{'file': 'app.java', 'method': 'badMethod()', 'line_number': '10'}] |
| thread_name | The name of the thread at fault | thread-1 |
| failure_time | The unix timestamp at which the failure occurs, in seconds | 1640966505.0 |
| app_id | The id of the failing app. They correspond to Table 1 of our paper. | 1 |
| app_version | The version of the app, denoted by the date they are tested in our device farm. | 2022-01-01 |
| device_brand | The brand of the failing device. For virtualized devices this is the brand of its physical device pair. | samsung |
| device_model | The device model of the failing device. The model for our virtualized devices is 'virt'. | samsung-model-1 |
| android_version | The android version of the device. | 10.0 |

## Running the Evaluation Script

You can run the evaluation script that produces the major figures and tables in our paper in two ways.

1. **(Recommended) Google Colab Notebook**
* Simply open [this notebook](https://colab.research.google.com/drive/19DYtr3yrJs6aKrXXyKWrBbMsCEvw46qw?usp=sharing). Under the `Runtime` tab, select `Run all`.
* The dependencies will be automatically configured. Please wait for ~3 minutes as the data are being processed.
* The figures and tables will be displayed in your browser.

1. Local Setup
* Clone this repository.
* Install [Python 3](https://www.python.org/downloads/) if you have not already. Then, run `pip3 install -r requirements.txt` at the root directory of this repo to install the dependencies.
* Run `python3 plot.py` at the root directory of this repo and wait for ~3 minutes as the data are being processed.
* A `fig/` directory will be created, and figures used in our paper can be found there. Tables will be printed to `stdout`.

## License

The failure data and its related scripts are made available under the GNU General Public License v3.0. By downloading it or using them, you agree to the terms of this license.
