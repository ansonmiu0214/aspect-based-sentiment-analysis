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

### Tagging Tool
Make sure there is no process running on **port 5000**. Use `lsof -i :5000` to check if this is the case.

```
$ cd tagging_tool/
$ python3 app.py
```
Tool accessible from **localhost:5000**.