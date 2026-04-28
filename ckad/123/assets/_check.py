#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
LAB_ID = os.path.basename(os.path.dirname(SCRIPT_DIR))
EXAM = os.path.basename(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
CLUSTER_NAME = f"{EXAM}-lab-{LAB_ID}"
NODE_NAME = f"{CLUSTER_NAME}-control-plane"

def docker_exec(*args):
    result = subprocess.run(
        ["docker", "exec", NODE_NAME, *args],
        capture_output=True, text=True,
    )
    return result

class TestCrictlImages(unittest.TestCase):
    def test_image_list_file_content(self):
        result = docker_exec("cat", "/opt/course/123/images")
        self.assertEqual(result.returncode, 0, "File /opt/course/123/images does not exist on the node")
        content = result.stdout
        self.assertIn("IMAGE ID", content, "File /opt/course/123/images does not seem to contain crictl images output (missing 'IMAGE ID' header)")
        self.assertIn("IMAGE", content, "File /opt/course/123/images does not seem to contain crictl images output (missing 'IMAGE' header)")

    def test_nginx_images_removed(self):
        result = docker_exec("sh", "-c", "crictl images -o json")
        data = json.loads(result.stdout)
        nginx_images = [img for img in data['images'] if any("nginx" in tag for tag in img.get('repoTags', []))]
        self.assertEqual(len(nginx_images), 0, f"Found {len(nginx_images)} nginx images on the node")

    def test_untagged_images_removed(self):
        result = docker_exec("sh", "-c", "crictl images -o json")
        data = json.loads(result.stdout)
        # Check for images with no tags or just <none>:<none>
        untagged_images = [img for img in data['images'] if not img.get('repoTags') or img.get('repoTags') == ["<none>:<none>"]]
        self.assertEqual(len(untagged_images), 0, f"Found {len(untagged_images)} untagged images on the node")

if __name__ == "__main__":
    unittest.main(verbosity=2)
