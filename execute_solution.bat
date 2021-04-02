python3 -m pip install virtualenv
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest --cov app
python3 main.py