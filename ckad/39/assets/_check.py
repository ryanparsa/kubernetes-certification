#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    # Use environment KUBECONFIG if set, otherwise fallback to local file
    env = os.environ.copy()
    if "KUBECONFIG" not in env and os.path.exists(KUBECONFIG_FILE):
        env["KUBECONFIG"] = KUBECONFIG_FILE

    cmd = ["kubectl", *args]
    result = subprocess.run(
        cmd,
        capture_output=True, text=True, env=env
    )
    return result.stdout.strip()

class TestPodDesign(unittest.TestCase):
    def test_namespace_exists(self):
        """Namespace pod-design exists"""
        ns = kubectl("get", "ns", "pod-design", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "pod-design")

    def test_deployment_spec(self):
        """Deployment frontend has 3 replicas and uses image nginx:1.19.0"""
        deploy_json = kubectl("get", "deployment", "frontend", "-n", "pod-design", "-o", "json")
        self.assertTrue(deploy_json, "Deployment frontend not found")
        deploy = json.loads(deploy_json)

        self.assertEqual(deploy["spec"]["replicas"], 3)
        self.assertEqual(deploy["spec"]["template"]["spec"]["containers"][0]["image"], "nginx:1.19.0")

    def test_labels(self):
        """Deployment and Pods carry labels app=frontend and tier=frontend"""
        deploy_json = kubectl("get", "deployment", "frontend", "-n", "pod-design", "-o", "json")
        deploy = json.loads(deploy_json)

        # Check deployment labels
        labels = deploy["metadata"]["labels"]
        self.assertEqual(labels.get("app"), "frontend")
        self.assertEqual(labels.get("tier"), "frontend")

        # Check pod template labels
        pod_labels = deploy["spec"]["template"]["metadata"]["labels"]
        self.assertEqual(pod_labels.get("app"), "frontend")
        self.assertEqual(pod_labels.get("tier"), "frontend")

    def test_service_spec(self):
        """Service frontend-svc is of type ClusterIP and exposes port 80"""
        svc_json = kubectl("get", "svc", "frontend-svc", "-n", "pod-design", "-o", "json")
        self.assertTrue(svc_json, "Service frontend-svc not found")
        svc = json.loads(svc_json)

        self.assertEqual(svc["spec"]["type"], "ClusterIP")
        self.assertEqual(svc["spec"]["ports"][0]["port"], 80)
        self.assertEqual(svc["spec"]["ports"][0]["targetPort"], 80)
        self.assertEqual(svc["spec"]["selector"].get("app"), "frontend")
        self.assertEqual(svc["spec"]["selector"].get("tier"), "frontend")

if __name__ == "__main__":
    unittest.main(verbosity=2)
