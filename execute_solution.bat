py -m pip install virtualenv
py -m venv venv
.\venv\Scripts\activate & pip install -r requirements.txt & pytest --cov app & py main.py