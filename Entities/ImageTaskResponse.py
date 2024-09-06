from flask import jsonify

class ImageTaskResponse:
    def __init__(self, msg: str, image_str: str = None):
        self.msg = msg
        self.image_str = image_str

    def to_jsonify(self) -> jsonify:
        data = {'msg': self.msg,
                'data': {
                    'image': self.image_str
                }}
        return jsonify(data)