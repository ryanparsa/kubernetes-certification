#!/usr/bin/env python3
import os
import subprocess
import unittest
import time

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
LAB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lab")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestUpdateCoreDNSConfiguration(unittest.TestCase):
    def test_backup_exists(self):
        filepath = os.path.join(LAB_DIR, "coredns_backup.yaml")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, 'r') as f:
            content = f.read()
        self.assertIn("kind: ConfigMap", content)
        self.assertIn("name: coredns", content)

    def test_dns_resolution(self):
        # Run a temporary pod to test DNS resolution
        pod_name = f"dns-test-pod-{time.time_ns()}"
        kubectl("run", pod_name, "--image=busybox:1", "--restart=Never", "--", "sleep", "3600")

        # Wait for pod to be ready
        for _ in range(30):
            status = kubectl("get", "pod", pod_name, "-o", "jsonpath={.status.phase}")
            if status == "Running":
                break
            time.sleep(2)
        else:
            self.fail("Test pod did not become ready in time")

        expected_ip = kubectl("get", "service", "kubernetes", "-o", "jsonpath={.spec.clusterIP}")
        self.assertTrue(expected_ip, "Could not determine kubernetes service clusterIP")

        try:
            # Test internal resolution
            out = kubectl("exec", pod_name, "--", "nslookup", "kubernetes.default.svc.cluster.local")
            self.assertIn(f"Address: {expected_ip}", out)

            # Test custom-domain resolution
            out = kubectl("exec", pod_name, "--", "nslookup", "kubernetes.default.svc.custom-domain")
            self.assertIn(f"Address: {expected_ip}", out)
        finally:
            kubectl("delete", "pod", pod_name, "--now")

if __name__ == "__main__":
    unittest.main(verbosity=2)
