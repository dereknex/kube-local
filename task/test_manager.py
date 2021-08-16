import unittest
import tempfile
from task import Manager
from config import Configuration
from input import Input
from output import Output


class TestManager(unittest.TestCase):
    test_cfg = """
auto_clean: true
local_path: temp/
inputs:
  - name: kubernetes
    kind: http
outputs:
  - name: kubernetes
    kind: s3
    bucket: kubernetes
    access_key: foo
    access_key_secret: bar
    endpoint: localhost:9000
    secure: false
tasks:
  - name: kubectl
    input: 
      name: kubernetes
      url: https://storage.googleapis.com/kubernetes-release/release/{{ version }}/bin/linux/{{ image_arch }}/kubectl
      sha256sum: "{{ sha256sum }}"
    output:
      name: kubernetes
      remote_prefix: "{{ version }}/linux/{{ image_arch }}/kubectl"
    with_items:
      - title: v1.21.3
        version: v1.21.3
        sha256sum: 603b6e57c5546c079faee6b606014e83b95ea076146fbf73329f3069968f83bf
        image_arch: arm
      - title: v1.21.2
        version: v1.21.2
        sha256sum: 898c2cd54b651873a8fb18bcb0792eb4772a78f845d758fa9b0eee278aede869
        image_arch: arm
"""

    def test_extract_item(self):
        item = {
            "version": "v1.21.2",
            "sha256sum": "898c2cd54b651873a8fb18bcb0792eb4772a78f845d758fa9b0eee278aede869",
            "image_arch": "arm",
        }
        in_dict = {
            "name": "kubernetes",
            "kind": "http",
            "url": "https://storage.googleapis.com/kubernetes-release/release/{{ version }}/bin/linux/{{ image_arch }}/kubectl",
            "sha256sum": "{{ sha256sum }}",
        }
        out_dict = {"name": "kubernetes", "kind": "s3", "remote_prefix": "{{ version }}/linux/{{ image_arch }}/kubectl"}
        f = tempfile.NamedTemporaryFile("w")
        f.writelines(self.test_cfg)
        f.flush()
        c = Configuration(f.name)
        m = Manager(c)
        # m._generate_tasks()
        i, o = m._extract_item(item, in_dict, out_dict)
        self.assertEqual(i.name, "kubernetes")
        self.assertEqual(o.name, "kubernetes")
        self.assertIsInstance(i, Input)
        self.assertIsInstance(o, Output)
        except_url = "https://storage.googleapis.com/kubernetes-release/release/v1.21.2/bin/linux/arm/kubectl"
        self.assertEqual(i.sha256sum, in_dict["sha256sum"])
        self.assertEqual(i.url, except_url)
        except_prefix = "v1.21.2/linux/arm/kubectl"
        self.assertEqual(o.remote_prefix, except_prefix)

    def test_generate_tasks(self):
        f = tempfile.NamedTemporaryFile("w")
        f.writelines(self.test_cfg)
        f.flush()
        c = Configuration(f.name)
        m = Manager(c)
        m._generate_tasks()
        self.assertEqual(len(m._tasks), 2, m._tasks)
        t1 = m._tasks[0]
        self.assertEqual(t1.name, "kubectl(v1.21.3)")
        except_url = "https://storage.googleapis.com/kubernetes-release/release/v1.21.3/bin/linux/arm/kubectl"
        self.assertEqual(t1.in_obj.url, except_url)
        t2 = m._tasks[1]
        self.assertEqual(t2.name, "kubectl(v1.21.2)")
        except_url = "https://storage.googleapis.com/kubernetes-release/release/v1.21.2/bin/linux/arm/kubectl"
        self.assertEqual(t2.in_obj.url, except_url)
