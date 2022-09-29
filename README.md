# Tech Assignment

[![python version](https://img.shields.io/badge/python-3.6+-brightgreen.svg)](https://www.python.org/downloads/)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The tech assignment repos contains the solution requested, the IaC and CI/CD.

## 📃 Table of Contents

- [🛠️ Install](#🛠️-install)
  - [📖 Prerequisites](#📖-prerequisites)
  - [🖥️ Local installation](#🖥️-local-installation)
- [🔬 Usage](#🔬-usage)
- [🧪 Test](#🧪-test)
- [👨‍💻 Deploy](#👨‍💻-deploy)
  - [☁️ Setting up a GCP Account](#☁️-setting-up-a-gcp-account)
  - [⚙️ Configuring secrets](#🔒-configuring-secrets)
  - [⚡ Deploying](#⚡-deploying)
  - [💣 Destroying](#💣-destroying)
  - [🧐 Checking the results](#🧐-Checking-the-results)
- [⚙️ CI/CD](#⚙️-CI/CD)
- [📐 Problem](#📐-problem)

## 🛠️ Install

### 📖 Prerequisites

- [Python](https://www.python.org/): I recommend using the official binaries provided by the Python Software Foundation.
- [Terraform](https://www.terraform.io): Optional, required for deploying to the cloud.
- [Google Cloud Platform](https://cloud.google.com): Optional, cloud vendor of choice, we will need to use some cli operations. You can use the web console instead.

### 🖥️ Local installation

There are no dependencies, so you don't need to pip install anything.

## 🔬 Usage

Running the python script with no arguments will prompt the user for either running the it with sample input, or providing the input inline.

```shell
# Run script
python src/main.py
```

You can choose to run the script with either the sample data or sample input which you need to provide data for link stations and devices.

```shell
# Sample data format
Use sample data? (y/n): n
Link Stations (x, y, reach): (0, 0, 10), (20, 20, 5), (10, 0, 12)
Devices (x, y): (0,0), (100,100), (15,10), (18,18)
```

## 🧪 Test

The unit tests are run using Python's built in unittest command.

```shell
# Run all tests
python -m unittest -v
```

## 👨‍💻 Deploy

A cloud configuration is already set up using [Terraform](https://www.terraform.io) and
[Google Cloud Platform](https://cloud.google.com). The Terraform configuration is under `terraform`.

The cloud infrastructure is minimal, and it consists of a Cloud Function which runs the script with the sample input
and returns the output as a response.

The steps below show some manual configurations you might need to do set up a Project successfully.

### ☁️ Setting up a GCP Account

If you are using the Google Cloud SDK for the first time, you will need to authenticate with your Google Account.
You can run the following command:

```shell
# Authenticate with GCP
gcloud auth application-default login
```

Now create the project on GCP:

```shell
# Create a GCP project
gcloud projects create PROJECT_ID --name="tech-assignment"
```

Set the project you just created as the default one. This will make it easier to run the subsequent commands.

```shell
# Set the project as the default one
gcloud config set project PROJECT_ID
```

### 🔒 Configuring secrets

Replace the variables in `variables.tf` to use your Project ID and GCP region. Please note that The Finland region (europe-north1) does not support Cloud Functions. You can check out more details about regions and available features per region [here](https://cloud.google.com/about/locations).

Aditionally, you need to change `versions.tf` to use your Google Cloud account.

On GitHub, you need to set up GCLOUD_CREDENTIALS and TF_API_TOKEN for CI/CD to work.

### ⚡ Deploying

Use the following commands to deploy the infrastructure to GCP:

```shell
# Deploy infrastructure to GCP
terraform apply
```

### 🧐 Checking the results

We can now check the results, we'll make a request at the link provided in the output or directly in the console in [Cloud Functions](https://console.cloud.google.com/functions/list). For testing, you can try out the cloud function I host at [https://europe-west1-tech-assignment-362812.cloudfunctions.net/my-function](https://europe-west1-tech-assignment-362812.cloudfunctions.net/my-function) using cURL or Postman for example.

cURL

```shell
curl -m 70 -X POST https://europe-west1-tech-assignment-362812.cloudfunctions.net/my-function -H "Content-Type:application/json" -d '{"link-stations":[{"x": 0,"y": 0,"reach": 10}],"devices": [{"x": 1,"y": 0}]}'
```

Example Request

```json
{
  "sample": false,
  "link-stations": [
    {
      "x": 0,
      "y": 0,
      "reach": 10
    }
  ],
  "devices": [
    {
      "x": 1,
      "y": 0
    }
  ]
}
```

Response

```shell
{
    {"body":"Best link station for point 1,0 is 0,0 with power 81.0\n","statusCode":200}
}
```

### 💣 Destroying

To delete the infrastructure we deployed, we can do so directly from Terraform and delete the the google project.

```shell
# Delete all infrastructure
terraform destroy

# Optional: delete the project
gcloud projects delete PROJECT_ID
```

## ⚙️ CI/CD

The pipelines are meant to check that the build is suitable, and once that is the case, it will deploy the infrastructure to GCP. The backend of choice where the state file is stored is Google Cloud, which is integrated in the pipelines. There's no Python linter unfortunately since it's dependency-free.

The pipelines are set up using [GitHub Actions](https://github.com/features/actions) and are located in `.github/workflows/`.

## 📐 Problem

Create a function that solves the most suitable (with most power) link station for a device at
given point [x,y].

Please write it in the language you know best, please also make this project as complete as you
think it should be to be maintainable in a long term by more than one maintainer.
This problem can be solved in 2-dimensional space. Link stations have reach and power.

A link station’s power can be calculated:

```
power = (reach - device's distance from link station)^2
if distance > reach, power = 0
```

Function receives list of link stations and the point where the device is located.
Function should output following line:

```
Best link station for point x,y is x,y with power z
```

or:

```
No link station within reach for point x,y
```

Link stations are located at points (x, y) and have reach (r) ([x, y, r]):

```
[[0, 0, 10],
[20, 20, 5],
[10, 0, 12]]
```

Print out function output from points (x, y):

```
(0,0), (100, 100), (15,10) and (18, 18).
```
