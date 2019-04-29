from unittest import TestCase, main
from json import loads
from base64 import b64decode

from screamshot.serializer import serialize, deserialize


class TestSerializerUnit(TestCase):
    def test_serialize_without_metadata(self):
        data = b'Hello world'
        json_data = serialize(data)

        self.assertIsInstance(json_data, str)

        extracted_data = loads(json_data)

        self.assertTrue('image' in extracted_data)
        self.assertFalse('metadata' in extracted_data)

        b64_image = extracted_data.get('image').encode('utf-8')
        self.assertNotEqual(data, b64_image)

        b_image = b64decode(b64_image)
        self.assertEqual(data, b_image)

    def test_serialize_with_metadata(self):
        data = b'Hello world'
        name = 'hello_world.png'
        author = 'John Doe'
        json_data = serialize(data, metadata={'name': name, 'author': author})

        extracted_data = loads(json_data)

        self.assertTrue('image' in extracted_data)
        self.assertTrue('metadata' in extracted_data)

        metadata = extracted_data.get('metadata')
        self.assertTrue('name' in metadata)
        self.assertTrue('author' in metadata)
        self.assertEqual(name, metadata.get('name'))
        self.assertEqual(author, metadata.get('author'))

        b64_image = extracted_data.get('image').encode('utf-8')
        self.assertNotEqual(data, b64_image)

        b_image = b64decode(b64_image)
        self.assertEqual(data, b_image)

    def test_deserialize_without_metadata(self):
        data = '{"image": "SGVsbG8gd29ybGQ="}'
        b_img, metadata = deserialize(data)

        self.assertIsInstance(b_img, bytes)
        self.assertIsInstance(metadata, dict)

        self.assertEqual(b_img, b'Hello world')
        self.assertEqual(metadata, {})

    def test_deserialize_with_metadata(self):
        data = '{"image": "SGVsbG8gd29ybGQ=", "metadata": {"name": "hello_world.png", \
            "author": "John Doe"}}'
        b_img, metadata = deserialize(data)

        self.assertIsInstance(b_img, bytes)
        self.assertIsInstance(metadata, dict)

        self.assertEqual(b_img, b'Hello world')
        self.assertEqual(metadata, {'name': 'hello_world.png', 'author': 'John Doe'})


if __name__ == '__main__':
    main()
