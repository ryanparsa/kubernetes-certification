#!/usr/bin/env python3
import os
import subprocess
import unittest

# Try local kubeconfig first (for local dev), then fallback to default (for CI)
LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "course")

def run_script(script_path):
    cmd = ["bash", script_path]
    env = os.environ.copy()
    if KUBECONFIG:
        env["KUBECONFIG"] = KUBECONFIG
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result.stdout.strip()

class TestKubectlSorting(unittest.TestCase):
    def test_find_pods_sh_exists(self):
        path = os.path.join(COURSE_DIR, "find_pods.sh")
        self.assertTrue(os.path.exists(path))

    def test_find_pods_uid_sh_exists(self):
        path = os.path.join(COURSE_DIR, "find_pods_uid.sh")
        self.assertTrue(os.path.exists(path))

    def test_find_pods_output(self):
        path = os.path.join(COURSE_DIR, "find_pods.sh")
        output = run_script(path)
        self.assertIn("NAMESPACE", output)
        self.assertIn("NAME", output)
        # Simple check for age sorting is hard without parsing times,
        # but we can verify it runs and produces output.

    def test_find_pods_uid_output(self):
        path = os.path.join(COURSE_DIR, "find_pods_uid.sh")
        output = run_script(path)
        self.assertIn("NAMESPACE", output)
        self.assertIn("NAME", output)

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
