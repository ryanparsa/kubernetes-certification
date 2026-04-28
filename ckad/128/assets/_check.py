#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
# Respect existing KUBECONFIG, fallback to local file
KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    env = os.environ.copy()
    env["KUBECONFIG"] = KUBECONFIG
    result = subprocess.run(
        ["kubectl", *args],
        capture_output=True, text=True, env=env
    )
    return result.stdout.strip()

class TestPlutoSidecar(unittest.TestCase):
    def test_deployment_has_sidecar(self):
        deployment_json = kubectl("get", "deployment", "pluto-deployment", "-n", "pluto", "-o", "json")
        self.assertTrue(deployment_json, "Could not get deployment pluto-deployment")
        deployment = json.loads(deployment_json)
        containers = deployment["spec"]["template"]["spec"]["containers"]
        sidecar = next((c for c in containers if c["name"] == "sidecar"), None)
        self.assertIsNotNone(sidecar, "Sidecar container not found")
        self.assertEqual(sidecar["image"], "busybox:1.31.0")
        self.assertIn("date >> /var/log/date.log", sidecar["command"][2])

    def test_shared_volume(self):
        deployment_json = kubectl("get", "deployment", "pluto-deployment", "-n", "pluto", "-o", "json")
        self.assertTrue(deployment_json, "Could not get deployment pluto-deployment")
        deployment = json.loads(deployment_json)
        containers = deployment["spec"]["template"]["spec"]["containers"]

        pluto_app = next((c for c in containers if c["name"] == "pluto-app"), None)
        sidecar = next((c for c in containers if c["name"] == "sidecar"), None)

        self.assertIsNotNone(pluto_app)
        self.assertIsNotNone(sidecar)

        pluto_mount = next((m for m in pluto_app.get("volumeMounts", []) if m["mountPath"] == "/tmp/log"), None)
        sidecar_mount = next((m for m in sidecar.get("volumeMounts", []) if m["mountPath"] == "/var/log"), None)

        self.assertIsNotNone(pluto_mount, "pluto-app does not mount /tmp/log")
        self.assertIsNotNone(sidecar_mount, "sidecar does not mount /var/log")
        self.assertEqual(pluto_mount["name"], sidecar_mount["name"], "Containers do not share the same volume")

if __name__ == "__main__":
    unittest.main(verbosity=2)
