# trading-analysis-investment
IB - viktad fördelning med hänsyn till störst substansrabatt. 

## Prerequisites
- Python 3.8
- pip
- Jupyter notebook
```sh
pip install notebook
```
-  [Virtual environment](https://docs.python.org/3/library/venv.html) 
-  [https://queirozf.com/entries/jupyter-kernels-how-to-add-change-remove](Create jupyter env kernel)
```sh
python3 -m venv env
```

## Installing
### Run virtual environment (mac)
```sh
cd <path/to/directory>
source env/bin/activate
```

### Install all dependancies in venv
```sh
pip install -r requirements.txt
```

### Run jupyter notebook
```sh
jupyter notebook
```
Open file IBStrategy.ipynb in browser

### Execute api
```sh
cd api
uvicorn main:app --reload
```

### Automatic docs (swagger)
Go to http://127.0.0.1:8000/docs