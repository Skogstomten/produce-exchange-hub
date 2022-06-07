# Setup local dev environment
## Requirements
- Python 3.10
- Visual Studio 2022
- Python editor of your choice

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
pip install -r requirements.txt
```

## Start
- Activate virtual environment
- Start api server
```
uvicorn app.main:app --reload
```
- Open web project in Visual Studio
- Start debugger with F5