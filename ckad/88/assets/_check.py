#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()

class TestNodeMonitor(unittest.TestCase):
    def test_daemonset_exists_and_running(self):
        """DaemonSet node-monitor exists and all pods are ready"""
        ds_json = kubectl("get", "ds", "node-monitor", "-n", "default", "-o", "json")
        self.assertTrue(ds_json != "", "DaemonSet node-monitor not found")
        ds = json.loads(ds_json)

        desired = ds["status"].get("desiredNumberScheduled", 0)
        ready = ds["status"].get("numberReady", 0)

        self.assertGreater(desired, 0, "Desired number of pods should be greater than 0")
        self.assertEqual(desired, ready, f"Not all pods are ready: {ready}/{desired}")

    def test_toleration_configured(self):
        """Toleration for control-plane is configured"""
        ds_json = kubectl("get", "ds", "node-monitor", "-n", "default", "-o", "json")
        ds = json.loads(ds_json)
        tolerations = ds["spec"]["template"]["spec"].get("tolerations", [])

        found = False
        for t in tolerations:
            if t.get("key") == "node-role.kubernetes.io/control-plane" and \
               t.get("operator") == "Exists" and \
               t.get("effect") == "NoSchedule":
                found = True
                break
        self.assertTrue(found, "Toleration for control-plane nodes not found")

    def test_resources_and_selector(self):
        """nodeSelector and resource requests are set correctly"""
        ds_json = kubectl("get", "ds", "node-monitor", "-n", "default", "-o", "json")
        ds = json.loads(ds_json)
        pod_spec = ds["spec"]["template"]["spec"]

        # nodeSelector
        self.assertEqual(pod_spec.get("nodeSelector", {}).get("kubernetes.io/os"), "linux")

        # resources
        container = pod_spec["containers"][0]
        requests = container.get("resources", {}).get("requests", {})
        self.assertEqual(requests.get("cpu"), "50m")
        self.assertEqual(requests.get("memory"), "32Mi")

if __name__ == "__main__":
    unittest.main(verbosity=2)
