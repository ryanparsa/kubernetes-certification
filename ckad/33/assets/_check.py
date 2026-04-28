#!/usr/bin/env python3

import os
import subprocess
import unittest

# Try local kubeconfig first (for local dev), then fallback to default (for CI)
LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestNodePortService(unittest.TestCase):

    def test_service_exists_with_type_nodeport(self):
        svc_type = kubectl("get", "svc", "public-web", "-n", "networking", "-o", "jsonpath={.spec.type}")
        self.assertEqual(svc_type, "NodePort")

    def test_service_selector_matches_web_frontend(self):
        selector = kubectl("get", "svc", "public-web", "-n", "networking", "-o", "jsonpath={.spec.selector.app}")
        self.assertEqual(selector, "web-frontend")

    def test_service_port_configuration(self):
        port = kubectl("get", "svc", "public-web", "-n", "networking", "-o", "jsonpath={.spec.ports[0].port}")
        target_port = kubectl("get", "svc", "public-web", "-n", "networking", "-o", "jsonpath={.spec.ports[0].targetPort}")
        node_port = kubectl("get", "svc", "public-web", "-n", "networking", "-o", "jsonpath={.spec.ports[0].nodePort}")
        self.assertEqual(port, "80")
        self.assertEqual(target_port, "8080")
        self.assertEqual(node_port, "30080")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
