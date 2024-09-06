from functools import wraps
from flask import Flask, request
from Entities.ImageTaskResponse import ImageTaskResponse

def key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        valid = request.headers.get('apiKey') == '807122cc6746e4c494116264c5a568b19ee7b86ef3867489850c95fc5fa927dd'
        if request.method == "POST" and valid:
            return f(*args, **kwargs)
        else:
            return ImageTaskResponse("Please provide an API key", None).to_jsonify(), 400
    return decorated