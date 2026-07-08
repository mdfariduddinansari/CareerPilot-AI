def success_response(data=None, message='OK'):
    return {'success': True, 'data': data, 'message': message, 'errors': []}
