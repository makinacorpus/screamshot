"""
serialize and deserialize functions
"""
from base64 import b64encode, b64decode
from json import dumps, loads
from typing import Tuple, Dict, Union


def serialize(img: bytes, metadata: dict = None) -> str:
    """
    This function serialize a binary bytes object

    :param img: mandatory, the binary bytes object
    :type img: bytes

    :param metadata: optional, some metadata about the object
    :type metadata: dict

    :return: a json formatted string containing the image and metadata
    :retype: str

    .. info :: In the json formatted string, the image is saved in base64 format
    """
    b64_img = b64encode(img)
    str_img = b64_img.decode('utf-8')
    data = {'image': str_img} #type: Dict[str, Union[str, Dict[str, str]]]
    if metadata:
        data.update({'metadata': metadata})
    json_img = dumps(data)
    return json_img


def deserialize(data: str) -> Tuple[bytes, dict]:
    """
    This function deserialize json formatted string

    :param data: the string json formatted string to deserialize
    :type data: str

    :return: the binary bytes image and metadata
    :retype: bytes, dict

    .. warning :: The data should look like the following example: \
        ``{"image": ..., "metadata": {...}}``
    """
    json_img = loads(data)
    str_img = json_img.get('image')
    metadata = json_img.get('metadata', {})
    b64_img = str_img.encode('utf-8')
    b_img = b64decode(b64_img)
    return b_img, metadata
