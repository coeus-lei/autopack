from fastapi import Request

def parse_headers(request: Request):
    headers = request.headers
    header_info = {header: value for header, value in headers.items()}
    return header_info

def parse_body(request: Request):
    body = request.json()
    return body
