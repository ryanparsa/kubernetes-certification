#!/usr/bin/env python3
import os
import subprocess
import unittest

LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_static_pod_name():
    pods = kubectl("get", "pods", "-n", "default",
                   "-o", "jsonpath={.items[*].metadata.name}").split()
    for p in pods:
        if p.startswith("my-static-pod-"):
            return p
    return ""


class TestStaticPodAndService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pod_name = get_static_pod_name()

    def test_static_pod_exists(self):
        self.assertTrue(self.pod_name, "Static pod my-static-pod-* not found in default namespace")

    def test_pod_has_single_container(self):
        if not self.pod_name:
            self.skipTest("No static pod found")
        containers = kubectl("get", "pod", self.pod_name, "-n", "default",
                             "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod_has_correct_image(self):
        if not self.pod_name:
            self.skipTest("No static pod found")
        image = kubectl("get", "pod", self.pod_name, "-n", "default",
                        "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")

    def test_pod_has_correct_cpu_requests(self):
        if not self.pod_name:
            self.skipTest("No static pod found")
        cpu = kubectl("get", "pod", self.pod_name, "-n", "default",
                      "-o", "jsonpath={.spec.containers[0].resources.requests.cpu}")
        self.assertEqual(cpu, "10m")

    def test_pod_has_correct_memory_requests(self):
        if not self.pod_name:
            self.skipTest("No static pod found")
        mem = kubectl("get", "pod", self.pod_name, "-n", "default",
                      "-o", "jsonpath={.spec.containers[0].resources.requests.memory}")
        self.assertEqual(mem, "20Mi")

    def test_service_is_nodeport(self):
        svc_type = kubectl("get", "svc", "static-pod-service", "-n", "default",
                           "-o", "jsonpath={.spec.type}")
        self.assertEqual(svc_type, "NodePort")

    def test_service_selector_matches_pod(self):
        if not self.pod_name:
            self.skipTest("No static pod found")
        # Service must have at least one endpoint (pod IP) to confirm selector matches
        endpoints = kubectl("get", "endpoints", "static-pod-service", "-n", "default",
                            "-o", "jsonpath={.subsets[*].addresses[*].ip}")
        self.assertTrue(endpoints,
                        "Service static-pod-service has no endpoints — selector may not match pod")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
