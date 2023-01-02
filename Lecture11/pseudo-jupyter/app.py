from flask import Flask, jsonify, request, redirect, send_from_directory
import logging
import os

import ipynb

# the main Flask application object
app = Flask(__name__)

# create logger instance
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

# global variables to store the current state of our notebook
inputs = ['print("Type your code snippet here")']
outputs = ['']
execute_counters = [0]
current_execute_count = 0


@app.route('/favicon.ico')
def favicon():
    """Handles browser's request for favicon"""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico'
    )


@app.route('/', methods=['GET'])
def get():
    """This triggers when you first open the site with your browser"""
    assert len(inputs) == len(outputs)
    return ipynb.render_notebook(inputs, outputs, execute_counters)


@app.route('/execute_cell/<cell_id>', methods=['POST'])
def execute(cell_id=None):
    """Gets piece of code from cell_id and executes it"""
    try:
        cell_id = int(cell_id)
    except ValueError as e:
        logger.warning(e)
        return redirect('/')

    global current_execute_count
    try:
        current_execute_count += 1
        execute_counters[cell_id] = current_execute_count
        
        inputs[cell_id] = request.form['input{}'.format(cell_id)]
        result = ipynb.execute_snippet(inputs[cell_id])
    except BaseException as e:
        # anything could happen inside, even `exit()` call
        result = str(e)

    outputs[cell_id] = result
    return redirect('/')


@app.route('/add_cell', methods=['POST'])
def add_cell():
    """Appends empty cell data to the end"""
    inputs.append('')
    outputs.append('')
    execute_counters.append(0)
    return redirect('/')


@app.route('/remove_cell/<cell_id>', methods=['POST'])
def remove_cell(cell_id=0):
    """Removes a cell by number"""
    try:
        cell_id = int(cell_id)
        if len(inputs) < 2:
            raise ValueError('Cannot remove the last cell')
        if cell_id < 0 or cell_id >= len(inputs):
            raise ValueError('Bad cell id')
    except ValueError as e:
        # do not change internal info
        logger.warning(e)
        return redirect('/')

    # remove related data
    inputs.pop(cell_id)
    outputs.pop(cell_id)
    execute_counters.pop(cell_id)
    return redirect('/')


@app.route('/ipynb', methods=['GET', 'POST'])
def ipynb_handler():
    """
    Imports/exports notebook data in .ipynb format (a.k.a Jupyter Notebook)
    Docs: https://nbformat.readthedocs.io/en/latest/format_description.html
    """
    global inputs
    global outputs
    if request.method == 'GET':
        # return json representation of the notebook here
        return ipynb.export(inputs, outputs)
    elif request.method == 'POST':
        # update internal data
        imported = ipynb.import_from_json(request.get_json())
        # we can return None if json is not a valid ipynb
        if imported:
            inputs, outputs = imported
        # common practice for POST/PUT is returning empty json
        # when everything is 200 OK
        return jsonify({})


# this makes your Flask application start
if __name__ == "__main__":
    app.run(debug=True)
