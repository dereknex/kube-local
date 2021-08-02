import unittest
import tempfile
from config import Configuration
from input import HTTPInput
from output import S3Output


class TestConfiguration(unittest.TestCase):
    def test_init(self):
        data = """
        auto_clean: true
        local_path: temp/
        inputs:
        outputs:
        tasks:
        """
        f = tempfile.NamedTemporaryFile("w")
        f.writelines(data)
        f.flush()
        c = Configuration(f.name)
        self.assertEqual("temp/", c.local_path)
        self.assertTrue(c.auto_clean)
        self.assertListEqual(c.inputs, [])
        self.assertListEqual(c.outputs, [])
        self.assertListEqual(c.tasks, [])

    def test_load_inputs(self):
        data = """
        auto_clean: true
        local_path: temp/
        inputs:
          - name: kubernetes
            type: http
        outputs:
        tasks:
        """
        f = tempfile.NamedTemporaryFile("w")
        f.writelines(data)
        f.flush()
        c = Configuration(f.name)
        self.assertEqual(1, len(c.inputs))
        i = c.inputs[0]
        self.assertIsInstance(i, HTTPInput)
        self.assertEqual(i.name, "kubernetes")

    def test_load_outputs(self):
        data = """
            auto_clean: true
            local_path: temp/
            inputs:
            outputs:
              - name: kubernetes
                type: s3
                bucket: kubernetes
                access_key: foo
                access_key_secret: bar
                endpoint: localhost:9000
                secure: false
            tasks:
            """
        f = tempfile.NamedTemporaryFile("w")
        f.writelines(data)
        f.flush()
        c = Configuration(f.name)
        self.assertEqual(1, len(c.outputs))
        o = c.outputs[0]
        self.assertIsInstance(o, S3Output)
        self.assertEqual(o.name, "kubernetes")
        self.assertEqual(o.bucket, "kubernetes")
        self.assertEqual(o.access_key, "foo")
        self.assertEqual(o.access_key_secret, "bar")
        self.assertEqual(o.endpoint, "localhost:9000")
        self.assertFalse(o.secure)
