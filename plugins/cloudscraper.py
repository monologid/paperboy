import cloudscraper


def execute(context, args):
    """
    CloudScraper plugin - to scrap a web or an API

    :param context:
    :param args:
    :return:
    """
    content_type = args['content_type']
    method = args['method']
    url = args['url']
    headers = args['headers'] if 'headers' in args else {}
    request_data = args['request_data'] if 'request_data' in args else {}

    if 'prev_result_id' in args:
        request_data = context['result'][args['prev_result_id']] if args['prev_result_id'] in context['result'] else {}

    scraper = cloudscraper.create_scraper()
    if str(method).lower() == 'post':
        response = scraper.post(url, data=request_data, headers=headers)
    elif str(method).lower() == 'put':
        response = scraper.put(url, data=request_data, headers=headers)
    elif str(method).lower() == 'patch':
        response = scraper.patch(url, data=request_data, headers=headers)
    elif str(method).lower() == 'delete':
        response = scraper.delete(url, data=request_data, headers=headers)
    else:
        response = scraper.get(url, params=request_data, headers=headers)

    if 200 >= response.status_code <= 299:
        if content_type == 'json':
            response = response.json()
        else:
            response = response.content()

        return {'success': True, 'data': response}

    return {'success': False, 'error': f"status_code={response.status_code}"}
