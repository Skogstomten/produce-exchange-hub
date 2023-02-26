# Project Description
## Purpose
The application is supposed to be a platform to help local, mainly small (but not limited to), farmers or other producers, to find and make contact with buyers, be it restaurants, grocery stores, other producers who require raw material for what they are producing, etc.

One can register a company, it can be either a buyer or producer or both. You can list what you have for sale, what quantity and other parameters and vice versa for buying. The application will automatically match producers with buyers for them to get in contact.

## Limitations
The application will not deal with transactions or delivery. It's only purpose (At least version 1) is to help the business find each other.

## System description
The latest iteration of the system is built in Python and Django.

# Setup local dev environment
## Requirements
- Python 3.10 or later.
- Python editor of your choice.

## Setup
- Clone repository
- Open console/powershell/terminal window at `X:/path/to/folder/produce-exchange-hub/farmers-market/farmers_market`
- Create virtual environment
```
python -m venv venv
```
- Activate virtual environment
```
.\venv\Scripts\activate
```
- Install dependencies
```
pip install -r requirements.txt
```

## Start
- Start api server
```
python manage.py runserver
```
Or Powershell script file
```
.\start.ps1
```

## Formatting
Black is being used for formatting with a line lenght of 121. While in active virtual environment with dev requirements loaded, run:
```
black ./ --line-length=121
```
Project folder contains a Powershell script file `format.ps1` with this script and hence, it's also possible to run:
```
.\format.ps1
```
