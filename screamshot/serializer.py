"""
serialize and deserialize functions
"""
from base64 import b64encode, b64decode
from typing import Tuple, Dict, Union


def serialize(img: bytes, metadata: dict = None) -> dict:
    """
    This function serialize a binary bytes object

    :param img: mandatory, the binary bytes object
    :type img: bytes

    :param metadata: optional, some metadata about the object
    :type metadata: dict

    :return: a dictionary containing the image and metadata
    :retype: str

    .. info :: The image is saved in base64 format
    """
    b64_img = b64encode(img)
    str_img = b64_img.decode('utf-8')
    data = {'image': str_img} #type: Dict[str, Union[str, Dict[str, str]]]
    if metadata:
        data.update({'metadata': metadata})
    return data


def deserialize(data: dict) -> Union[Tuple[None, None], Tuple[bytes, dict]]:
    """
    This function deserialize a dictionary

    :param data: the dictionary to deserialize
    :type data: str

    :return: the binary bytes image and metadata
    :retype: bytes, dict

    .. warning :: The data should look like the following example: \
        ``{"image": ..., "metadata": {...}}`` or ``None, None`` is returned
    """
    str_img = data.get('image')
    if str_img:
        metadata = data.get('metadata', {})
        b64_img = str_img.encode('utf-8')
        b_img = b64decode(b64_img)
        return b_img, metadata
    return None, None
