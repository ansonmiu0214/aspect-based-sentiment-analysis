# aspect-based-sentiment-analysis

## Getting started

### Prerequisites
Python 3.7.0

### First-time setup
Initialise a virtual environment and install dependencies from `requirements.txt`.
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt 
```

### Setting up with PyCharm
Locate the "Project Structure" menu in Preferences and set `src/` as a source folder.
Not doing so may lead to errors in the import statements.

### Tagging Tool
Make sure there is no process running on **port 5000**. Use `lsof -i :5000` to check if this is the case.

```
$ cd tagging_tool/
$ python3 app.py
```
Tool accessible from **localhost:5000**.

### Demo
Set up Flask by running the following:
```
cd src/
export FLASK_APP=flaskapp.py
flask run
```
This runs the Flask backend on **localhost:5000**.

In a separate terminal, run:
```
  cd demo/
  npm install
  npm run
```

Your browser should open and point to **localhost:3000**.
