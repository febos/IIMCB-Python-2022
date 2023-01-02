# Pseudo Jupyter Notebook
### demo on Flask&HTML (IIMCB 2023)


### Flask official tutorial:
http://flask.pocoo.org/docs/1.0/tutorial/


### Usage:
```
pip3 install flask
python3 app.py
```

Follow localhost address in your console (most likely http://127.0.0.1:5000)

### Note:

It's a fake Jupyter, because it does not:
- keep the state between cells
- import notebooks with Markdown and other special types of cells
- export or import to files directly...
- ...but it's possible with a secret `/ipynb` route and some simple shell magic (see `tests/` dir)

Pull requests are welcome :)
