from unittest import TestCase, main
from base64 import b64decode

from screamshot.serializer import serialize, deserialize


class TestSerializerUnit(TestCase):
    def test_serialize_without_metadata(self):
        data = b'Hello world'
        dict_data = serialize(data)

        self.assertIsInstance(dict_data, dict)

        self.assertTrue('image' in dict_data)
        self.assertFalse('metadata' in dict_data)

        b64_image = dict_data.get('image').encode('utf-8')
        self.assertNotEqual(data, b64_image)

        b_image = b64decode(b64_image)
        self.assertEqual(data, b_image)

    def test_serialize_with_metadata(self):
        data = b'Hello world'
        name = 'hello_world.png'
        author = 'John Doe'
        dict_data = serialize(data, metadata={'name': name, 'author': author})

        self.assertIsInstance(dict_data, dict)

        self.assertTrue('image' in dict_data)
        self.assertTrue('metadata' in dict_data)

        metadata = dict_data.get('metadata')
        self.assertTrue('name' in metadata)
        self.assertTrue('author' in metadata)
        self.assertEqual(name, metadata.get('name'))
        self.assertEqual(author, metadata.get('author'))

        b64_image = dict_data.get('image').encode('utf-8')
        self.assertNotEqual(data, b64_image)

        b_image = b64decode(b64_image)
        self.assertEqual(data, b_image)

    def test_deserialize_without_metadata(self):
        data = {"image": "SGVsbG8gd29ybGQ="}
        b_img, metadata = deserialize(data)

        self.assertIsInstance(b_img, bytes)
        self.assertIsInstance(metadata, dict)

        self.assertEqual(b_img, b'Hello world')
        self.assertEqual(metadata, {})

    def test_deserialize_with_metadata(self):
        data = {"image": "SGVsbG8gd29ybGQ=", "metadata": {"name": "hello_world.png",
                                                          "author": "John Doe"}}
        b_img, metadata = deserialize(data)

        self.assertIsInstance(b_img, bytes)
        self.assertIsInstance(metadata, dict)

        self.assertEqual(b_img, b'Hello world')
        self.assertEqual(
            metadata, {'name': 'hello_world.png', 'author': 'John Doe'})

    def test_deserialize_bad_object(self):
        data = {}
        b_img, metadata = deserialize(data)
        self.assertFalse(b_img)
        self.assertFalse(metadata)


if __name__ == '__main__':
    main()
