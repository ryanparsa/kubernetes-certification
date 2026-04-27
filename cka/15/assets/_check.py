#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def get_pod_ip(pod_name, namespace):
    return kubectl("get", "pod", pod_name, "-n", namespace, "-o", "jsonpath={.status.podIP}")


def can_connect(src_pod, namespace, target_ip, port, timeout=5):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG,
         "exec", src_pod, "-n", namespace, "--",
         "curl", "-s", "--connect-timeout", str(timeout), f"{target_ip}:{port}"],
        capture_output=True, text=True,
    )
    return result.returncode == 0


class TestNetworkPolicy(unittest.TestCase):

    def test_networkpolicy_exists(self):
        """NetworkPolicy np-backend exists in namespace project-snake"""
        name = kubectl("get", "networkpolicy", "np-backend", "-n", "project-snake",
                       "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "np-backend")

    def test_statefulsets_exist_and_ready(self):
        """StatefulSets backend, db1, db2 and vault exist and are ready"""
        for name in ["backend", "db1", "db2", "vault"]:
            ready = kubectl("get", "statefulset", name, "-n", "project-snake",
                            "--ignore-not-found", "-o", "jsonpath={.status.readyReplicas}")
            self.assertEqual(ready, "1", f"StatefulSet {name} is not ready (readyReplicas={ready!r})")

    def test_backend_can_reach_db1_port_1111(self):
        """Backend can reach db1 on port 1111"""
        db1_ip = get_pod_ip("db1-0", "project-snake")
        self.assertTrue(can_connect("backend-0", "project-snake", db1_ip, 1111),
                        f"backend-0 should be able to reach db1-0 ({db1_ip}) on port 1111")

    def test_backend_cannot_reach_db1_other_ports(self):
        """Backend can reach db1 only on port 1111"""
        db1_ip = get_pod_ip("db1-0", "project-snake")
        self.assertFalse(can_connect("backend-0", "project-snake", db1_ip, 2222),
                         f"backend-0 should NOT be able to reach db1-0 ({db1_ip}) on port 2222")

    def test_backend_can_reach_db2_port_2222(self):
        """Backend can reach db2 on port 2222"""
        db2_ip = get_pod_ip("db2-0", "project-snake")
        self.assertTrue(can_connect("backend-0", "project-snake", db2_ip, 2222),
                        f"backend-0 should be able to reach db2-0 ({db2_ip}) on port 2222")

    def test_backend_cannot_reach_db2_other_ports(self):
        """Backend can reach db2 only on port 2222"""
        db2_ip = get_pod_ip("db2-0", "project-snake")
        self.assertFalse(can_connect("backend-0", "project-snake", db2_ip, 1111),
                         f"backend-0 should NOT be able to reach db2-0 ({db2_ip}) on port 1111")

    def test_backend_cannot_reach_vault(self):
        """Backend cannot reach vault on any port"""
        vault_ip = get_pod_ip("vault-0", "project-snake")
        self.assertFalse(can_connect("backend-0", "project-snake", vault_ip, 3333),
                         f"backend-0 should NOT be able to reach vault-0 ({vault_ip}) on any port")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
