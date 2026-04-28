#!/usr/bin/env python3

import json
import os
import subprocess
import unittest

LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def helm(*args):
    cmd = ["helm"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


class TestHelmBitnamiNginx(unittest.TestCase):

    def test_bitnami_repo_added(self):
        output = helm("repo", "list", "-o", "json")
        repos = json.loads(output) if output else []
        names = [r["name"] for r in repos]
        self.assertIn("bitnami", names)

    def test_nginx_chart_deployed_with_2_replicas(self):
        replicas = kubectl(
            "get", "deployment", "-n", "web",
            "-o", "jsonpath={.items[?(@.metadata.labels['app\\.kubernetes\\.io/name']==\"nginx\")].spec.replicas}",
        )
        self.assertEqual(replicas, "2")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
