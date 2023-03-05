# trading-analysis-investment
API and APP for analysing swedish investment companies

## Prerequisites
- Python >= 3.8
- pip
- ~~Jupyter notebook~~ DEPRECATED
-  [Virtual environment wrapper installing instructions](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) 
```sh
## Install virtual environment wrapper using pip (setup shell startup according to installing instructions)
pip install virtualenvwrapper

## create virtualenvwrapper
mkvirtualenv venv

## run virtualenvironment
workon venv

## quit virtualenv
deactivate venv
```

## Installing
### Install all dependancies in venv
```sh
workon venv
pip install -r requirements.txt
```

### Execute api
```sh
cd api
uvicorn main:app --reload
```
### Automatic api docs (swagger)
Go to http://127.0.0.1:8000/docs

[Latest database model can be found here](https://robinmori.github.io/trading-analysis-investment/embed.html)

### Run app
```sh
cd app
npm install
npm run dev
```
