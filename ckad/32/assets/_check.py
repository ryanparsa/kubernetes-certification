#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestClusterIPService(unittest.TestCase):

    def test_service_exists_with_type_clusterip(self):
        svc_type = kubectl(
            "get", "svc", "internal-app", "-n", "networking",
            "-o", "jsonpath={.spec.type}",
        )
        self.assertEqual(svc_type, "ClusterIP")

    def test_service_selector_matches_backend(self):
        selector = kubectl(
            "get", "svc", "internal-app", "-n", "networking",
            "-o", "jsonpath={.spec.selector.app}",
        )
        self.assertEqual(selector, "backend")

    def test_service_port_and_target_port(self):
        port = kubectl(
            "get", "svc", "internal-app", "-n", "networking",
            "-o", "jsonpath={.spec.ports[0].port}",
        )
        target_port = kubectl(
            "get", "svc", "internal-app", "-n", "networking",
            "-o", "jsonpath={.spec.ports[0].targetPort}",
        )
        self.assertEqual(port, "80")
        self.assertEqual(target_port, "8080")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
