from base64 import b64encode, b64decode
from json import dumps, loads


def serialize(img: bytes, metadata: dict = None) -> str:
    b64_img = b64encode(img)
    str_img = b64_img.decode('utf-8')
    json_img = dumps({'image': str_img})
    return json_img


def deserialize(data: str) -> bytes:
    json_img = loads(data)
