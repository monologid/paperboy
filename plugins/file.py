import json


def execute(context, args):
    """
    File plugin - to save data to a file

    :param context:
    :param args:
    :return:
    """
    content_type = args['content_type']
    file_path = args['file_path']

    if 'prev_result_id' in args:
        prev_result_id = args['prev_result_id']
        data = context['result'][prev_result_id]
    else:
        data = args['data'] if 'data' in args else {}

    if content_type == 'json':
        data = json.dumps(data)

    file = open(file_path, 'w')
    file.write(data)
    file.close()

    return {'success': True}
