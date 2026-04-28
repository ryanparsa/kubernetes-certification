#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TASK_DIR = os.path.dirname(SCRIPT_DIR)
LAB_ID = os.path.basename(TASK_DIR)
EXAM = os.path.basename(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
CLUSTER_NAME = f"{EXAM}-lab-{LAB_ID}"
KUBECONFIG = os.path.join(TASK_DIR, "lab", "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

class TestCoreDNSUpdate(unittest.TestCase):
    def test_backup_exists(self):
        # Check if backup file exists on the control-plane node
        result = subprocess.run([
            "docker", "exec", f"{CLUSTER_NAME}-control-plane",
            "ls", "/opt/course/95/coredns-backup.yaml"
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Backup file /opt/course/95/coredns-backup.yaml not found on control-plane node")

    def test_configmap_updated(self):
        # Check if ConfigMap contains the forward rule
        result = kubectl("-n", "kube-system", "get", "cm", "coredns", "-o", "json")
        self.assertEqual(result.returncode, 0)
        cm = json.loads(result.stdout)
        corefile = cm.get("data", {}).get("Corefile", "")
        self.assertIn("very-secure.io", corefile, "very-secure.io not found in Corefile")
        self.assertIn("forward . 1.2.3.4", corefile, "Forward rule to 1.2.3.4 not found in Corefile")

    def test_coredns_pods_running(self):
        # Check if CoreDNS pods are running and using the new config (rollout finished)
        result = kubectl("-n", "kube-system", "get", "pods", "-l", "k8s-app=kube-dns", "-o", "json")
        self.assertEqual(result.returncode, 0)
        pods = json.loads(result.stdout)
        self.assertTrue(len(pods.get("items", [])) > 0, "No CoreDNS pods found")
        for pod in pods["items"]:
            status = pod.get("status", {}).get("phase", "")
            self.assertEqual(status, "Running", f"Pod {pod['metadata']['name']} is not Running")

if __name__ == "__main__":
    unittest.main(verbosity=2)
