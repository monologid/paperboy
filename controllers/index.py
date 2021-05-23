from flask import Blueprint, render_template

root = Blueprint('index', __name__)


@root.route('/', methods=['GET'])
def index():
    return render_template('index.html')
