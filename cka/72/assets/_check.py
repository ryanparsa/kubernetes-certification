#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_DIR = os.path.join(SCRIPT_DIR, "..", "course")

def get_kubeconfig():
    if "KUBECONFIG" in os.environ:
        return os.environ["KUBECONFIG"]
    local_kubeconfig = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
    if os.path.exists(local_kubeconfig):
        return local_kubeconfig
    return os.path.expanduser("~/.kube/config")

def kubectl(*args):
    env = os.environ.copy()
    env["KUBECONFIG"] = get_kubeconfig()

    result = subprocess.run(
        ["kubectl", *args],
        capture_output=True, text=True, env=env
    )
    return result.stdout.strip()

class TestContexts(unittest.TestCase):
    def test_contexts_file(self):
        filepath = os.path.join(COURSE_DIR, "contexts")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, "r") as f:
            content = f.read().splitlines()

        expected_contexts = kubectl("config", "get-contexts", "-o", "name").splitlines()
        self.assertCountEqual(content, expected_contexts)

    def test_kubectl_command_file(self):
        filepath = os.path.join(COURSE_DIR, "context_default_kubectl")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, "r") as f:
            command = f.read().strip()

        env = os.environ.copy()
        env["KUBECONFIG"] = get_kubeconfig()

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, env=env
        )
        output = result.stdout.strip()
        current_context = kubectl("config", "current-context")
        self.assertEqual(output, current_context)
        self.assertIn("kubectl", command)

    def test_sh_command_file(self):
        filepath = os.path.join(COURSE_DIR, "context_default_sh")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, "r") as f:
            command = f.read().strip()

        env = os.environ.copy()
        env["KUBECONFIG"] = get_kubeconfig()

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, env=env
        )
        output = result.stdout.strip()
        current_context = kubectl("config", "current-context")
        self.assertEqual(output, current_context)
        self.assertNotIn("kubectl", command)

if __name__ == "__main__":
    unittest.main(verbosity=2)
