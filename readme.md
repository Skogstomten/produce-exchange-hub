# Project Description
## Purpose
The application is supposed to be a platform to help local, mainly small (but not limited to), farmers or other producers, to find and make contact with buyers, be it restaurants, grocery stores, other producers who require raw material for what they are producing, etc.

One can register a company, it can be either a buyer or producer or both. You can list what you have for sale, what quantity and other parameters and vice versa for buying. The application will automatically match producers with buyers for them to get in contact.

## Limitations
The application will not deal with transactions or delivery. It's only purpose (At least version 1) is to help the business find each other.

## System description
The application is made up mainly two components at the time of writing.
### API
Api is to handle all logic and authentication. It implements an oauth2 protocol for authentication and also provides the identity manager.
It's built in python with [FastAPI](https://fastapi.tiangolo.com/)
Database is currently cloud based [MongoDB](https://www.mongodb.com/)
  - This might be changed if there's accessibility issues.
### Web
It is being built as a [Blazor WebAssembly](https://dotnet.microsoft.com/en-us/apps/aspnet/web-apps/blazor) app. Currently it's in a very early stage of development as more work has been put on the business logic in the api.

# Setup local dev environment
## Requirements
- Python 3.10
- Visual Studio 2022
- Python editor of your choice (pycharm is nice)

## Setup
- Clone repository
- Open console/powershell/terminal window at `X:/path/to/folder/produce-exchange-hub/api`
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
pip install -r requirements.dev.txt
```

## Start
- Activate virtual environment
- Start api server
```
uvicorn app.main:app --reload
```
- Open web project in Visual Studio
- Start debugger with F5

## Formatting API
Black is being used for formatting with a line lenght of 121. While in active virtual environment with dev requirements loaded, run:
```
black app --line-length=121
black tests --line-length=121
```

## Local DB
It is possible to run the application towards the cloud db or local db. Local DB is recommended during development.
To setup local db, install MongoDB server Community edition and create a local connection with local account login.
Run the application `./tools/remote_db_cloner/main.py`
This should copy all data from remote DB to your local DB.
