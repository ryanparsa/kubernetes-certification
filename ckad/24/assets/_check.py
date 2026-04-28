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


class TestConfigMapAndPodWithResources(unittest.TestCase):

    def test_configmap_exists_with_correct_data(self):
        app_env = kubectl("get", "configmap", "app-config", "-n", "workloads",
                          "-o", "jsonpath={.data.APP_ENV}")
        self.assertEqual(app_env, "production")
        log_level = kubectl("get", "configmap", "app-config", "-n", "workloads",
                            "-o", "jsonpath={.data.LOG_LEVEL}")
        self.assertEqual(log_level, "info")

    def test_pod_is_running(self):
        phase = kubectl("get", "pod", "config-pod", "-n", "workloads",
                        "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod_env_vars_sourced_from_configmap(self):
        app_env_ref = kubectl("get", "pod", "config-pod", "-n", "workloads",
                              "-o", "jsonpath={.spec.containers[0].env[?(@.name==\"APP_ENV\")].valueFrom.configMapKeyRef.name}")
        self.assertEqual(app_env_ref, "app-config")
        log_level_ref = kubectl("get", "pod", "config-pod", "-n", "workloads",
                                "-o", "jsonpath={.spec.containers[0].env[?(@.name==\"LOG_LEVEL\")].valueFrom.configMapKeyRef.name}")
        self.assertEqual(log_level_ref, "app-config")

    def test_pod_resource_requests_and_limits(self):
        cpu_req = kubectl("get", "pod", "config-pod", "-n", "workloads",
                          "-o", "jsonpath={.spec.containers[0].resources.requests.cpu}")
        self.assertEqual(cpu_req, "100m")
        cpu_lim = kubectl("get", "pod", "config-pod", "-n", "workloads",
                          "-o", "jsonpath={.spec.containers[0].resources.limits.cpu}")
        self.assertEqual(cpu_lim, "200m")
        mem_req = kubectl("get", "pod", "config-pod", "-n", "workloads",
                          "-o", "jsonpath={.spec.containers[0].resources.requests.memory}")
        self.assertEqual(mem_req, "128Mi")
        mem_lim = kubectl("get", "pod", "config-pod", "-n", "workloads",
                          "-o", "jsonpath={.spec.containers[0].resources.limits.memory}")
        self.assertEqual(mem_lim, "256Mi")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
