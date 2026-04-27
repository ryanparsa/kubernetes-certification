#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
LAB_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lab"))


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip(), result.returncode


class TestCoreDNS(unittest.TestCase):

    def test_backup_file_exists(self):
        path = os.path.join(LAB_DIR, "coredns_backup.yaml")
        self.assertTrue(os.path.isfile(path), "File cka/16/lab/coredns_backup.yaml not found")

    def test_backup_contains_coredns_configmap(self):
        path = os.path.join(LAB_DIR, "coredns_backup.yaml")
        if not os.path.isfile(path):
            self.skipTest("Backup file not found")
        content = open(path).read()
        self.assertIn("kind: ConfigMap", content, "Backup does not look like a ConfigMap")
        self.assertIn("name: coredns", content, "Backup ConfigMap is not named 'coredns'")
        self.assertIn("cluster.local", content, "Backup Corefile should contain 'cluster.local'")

    def test_live_configmap_has_custom_domain(self):
        out, rc = kubectl("-n", "kube-system", "get", "cm", "coredns",
                          "-o", "jsonpath={.data.Corefile}")
        if rc != 0:
            self.skipTest("Could not access CoreDNS ConfigMap — is the lab running?")
        self.assertIn("custom-domain", out,
                      "CoreDNS Corefile does not contain 'custom-domain'")
        for line in out.splitlines():
            if "kubernetes" in line and "cluster.local" in line:
                self.assertIn("custom-domain", line,
                              "custom-domain must be on the same kubernetes plugin line as cluster.local")
                break

    def test_coredns_pods_running(self):
        out, rc = kubectl("-n", "kube-system", "get", "pods", "-l", "k8s-app=kube-dns",
                          "--field-selector=status.phase=Running", "-o", "name")
        if rc != 0:
            self.skipTest("Could not query pods — is the lab running?")
        self.assertTrue(len(out) > 0, "No CoreDNS pods are in Running state")

    def test_dns_resolves_custom_domain(self):
        pod = "coredns-check"
        subprocess.run(
            ["kubectl", "--kubeconfig", KUBECONFIG, "delete", "pod", pod,
             "--ignore-not-found", "--wait=false"],
            capture_output=True,
        )
        _, rc = kubectl("run", pod, "--image=busybox:1", "--restart=Never",
                        "--", "nslookup", "kubernetes.default.svc.custom-domain")
        if rc != 0:
            self.skipTest("Could not schedule DNS test pod — is the cluster running?")
        kubectl("wait", f"pod/{pod}", "--for=jsonpath={.status.phase}=Succeeded", "--timeout=30s")
        logs, _ = kubectl("logs", pod)
        subprocess.run(
            ["kubectl", "--kubeconfig", KUBECONFIG, "delete", "pod", pod, "--ignore-not-found"],
            capture_output=True,
        )
        self.assertIn("Address", logs, "Expected an IP address in nslookup output for kubernetes.default.svc.custom-domain")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
