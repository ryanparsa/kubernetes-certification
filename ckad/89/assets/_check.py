#!/usr/bin/env python3
import os
import subprocess
import unittest
import json
import sys

# Use environment KUBECONFIG if set, otherwise use local one
KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()

class TestJobConfiguration(unittest.TestCase):
    def setUp(self):
        self.job_json = kubectl("get", "job", "neb-new-job", "-n", "neptune", "-o", "json")
        if self.job_json is None:
            self.job = None
        else:
            try:
                self.job = json.loads(self.job_json)
            except json.JSONDecodeError:
                self.job = None

    def test_job_exists(self):
        self.assertIsNotNone(self.job, "Job neb-new-job does not exist in namespace neptune or could not be retrieved")
        self.assertEqual(self.job["metadata"]["name"], "neb-new-job")
        self.assertEqual(self.job["metadata"]["namespace"], "neptune")

    def test_job_spec(self):
        self.assertIsNotNone(self.job)
        spec = self.job["spec"]
        self.assertEqual(spec.get("completions"), 3)
        self.assertEqual(spec.get("parallelism"), 2)
        self.assertEqual(spec.get("activeDeadlineSeconds"), 30)

    def test_container_configuration(self):
        self.assertIsNotNone(self.job)
        container = self.job["spec"]["template"]["spec"]["containers"][0]
        self.assertEqual(container["name"], "neb-new-job-container")
        self.assertEqual(container["image"], "busybox:1.31.0")
        self.assertEqual(container["command"], ["sh", "-c", "sleep 2 && echo done"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
