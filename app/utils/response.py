def success_message(message: str, data: dict = None):
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return response

def error_message(message: str, details: str = None):
    response = {"success": False, "message": message}
    if details is not None:
        response["details"] = details
    return response