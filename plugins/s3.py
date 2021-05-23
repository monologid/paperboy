import io
import json
from minio import Minio


def execute(context, args):
    """
    S3 plugin - to upload data/file into S3-support storage

    :param context:
    :param args:
    :return:
    """
    content_type = args['content_type']
    bucket = args['bucket']
    object_file = args['object']
    metadata = args['metadata'] if 'metadata' in args else {}
    part_size = 10*1024*1024

    host = args['host']
    access_key = args['access_key']
    secret_key = args['secret_key']
    s3client = Minio(host, access_key, secret_key)

    if 'prev_result_id' in args:
        prev_result_id = args['prev_result_id']
        data = context['result'][prev_result_id]
    else:
        data = args['data'] if 'data' in args else {}

    if content_type == 'json':
        data = io.BytesIO(str.encode(json.dumps(data)))
        content_type = 'application/json'
    else:
        content_type = 'application/text'

    try:
        s3client.put_object(
            bucket_name=bucket,
            object_name=object_file,
            content_type=content_type,
            data=data,
            length=-1,
            part_size=part_size,
            metadata=metadata
        )

        url = f"{host}/{bucket}/{object_file}"
        return {'success': True, 'data': url}
    except Exception as e:
        return {'success': False, 'error': e}
