#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

class TestApiIngress(unittest.TestCase):
    def test_ingress_exists(self):
        """Ingress api-ingress exists in namespace networking"""
        result = kubectl("get", "ingress", "api-ingress", "-n", "networking")
        self.assertEqual(result.returncode, 0, "Ingress api-ingress not found in namespace networking")

    def test_ingress_host(self):
        """Ingress routes traffic for host api.example.com"""
        result = kubectl("get", "ingress", "api-ingress", "-n", "networking", "-o", "json")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        rules = data.get("spec", {}).get("rules", [])
        hosts = [rule.get("host") for rule in rules if "host" in rule]
        self.assertIn("api.example.com", hosts, "Ingress does not have rule for host api.example.com")

    def test_ingress_backend(self):
        """Ingress backend points to service api-service on port 80"""
        result = kubectl("get", "ingress", "api-ingress", "-n", "networking", "-o", "json")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        rules = data.get("spec", {}).get("rules", [])

        found = False
        for rule in rules:
            if rule.get("host") == "api.example.com":
                http = rule.get("http", {})
                paths = http.get("paths", [])
                for path in paths:
                    backend = path.get("backend", {})
                    service = backend.get("service", {})
                    if service.get("name") == "api-service":
                        port = service.get("port", {})
                        if port.get("number") == 80:
                            found = True
                            break
        self.assertTrue(found, "Ingress backend for api.example.com does not point to api-service on port 80")

if __name__ == "__main__":
    unittest.main(verbosity=2)
