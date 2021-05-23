from flask import Blueprint, request
from common import constant
from database import DB
import json
import os


api_job_v1 = Blueprint('api_job_v1', __name__, url_prefix='/api/v1/job')


@api_job_v1.route('', methods=['GET'])
def get():
    data = []
    temp_data = os.listdir('tasks')
    for filename in temp_data:
        if filename != '.gitkeep':
            data.append(str(filename).replace('.json', ''))

    return {'success': True, 'data': data}


@api_job_v1.route('/<job_id>', methods=['GET'])
def get_by_id(job_id: str):
    filepath = f"tasks/{job_id}.json"
    try:
        file = open(filepath, 'r')
        data = json.loads(file.read())
        file.close()
        return {'success': True, 'data': data}
    except Exception as e:
        return {'success': False}


@api_job_v1.route('', methods=['POST'])
def create():
    data = request.get_json(force=True)
    task_name = data[u'name']
    filepath = f"tasks/{task_name}.json"
    file = open(filepath, 'w')
    file.write(json.dumps(data))
    file.close()

    tasks = []
    results = DB.get(constant.KeyTasks)
    if results is None:
        tasks.append(task_name)
        DB.set(constant.KeyTasks, json.dumps(tasks))
    else:
        tasks = json.loads(results)
        if task_name not in tasks:
            tasks.append(task_name)
        DB.set(constant.KeyTasks, json.dumps(tasks))

    return {'success': True}
