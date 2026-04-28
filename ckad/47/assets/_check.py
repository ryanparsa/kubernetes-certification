#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if "KUBECONFIG" not in os.environ and os.path.exists(KUBECONFIG_FILE):
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestSecureApp(unittest.TestCase):
    def test_namespace_exists(self):
        ns = kubectl("get", "namespace", "security", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "security")

    def test_pod_exists_and_image(self):
        image = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx:alpine")

    def test_pod_command(self):
        command = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.containers[0].command[0]}")
        self.assertEqual(command, "sleep")
        args = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.containers[0].command[1]}")
        self.assertEqual(args, "3600")

    def test_pod_security_context(self):
        # Pod level runAsUser
        run_as_user = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.securityContext.runAsUser}")
        self.assertEqual(run_as_user, "1000")

        # runAsNonRoot can be at Pod or Container level
        pod_level = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.securityContext.runAsNonRoot}")
        container_level = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.containers[0].securityContext.runAsNonRoot}")
        self.assertTrue(pod_level == "true" or container_level == "true")

    def test_container_security_context(self):
        # Container level capabilities
        capabilities_drop = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.containers[0].securityContext.capabilities.drop[*]}")
        self.assertIn("ALL", capabilities_drop)

        # Container level readOnlyRootFilesystem
        read_only_root_fs = kubectl("get", "pod", "secure-app", "-n", "security", "-o", "jsonpath={.spec.containers[0].securityContext.readOnlyRootFilesystem}")
        self.assertEqual(read_only_root_fs, "true")

if __name__ == "__main__":
    unittest.main()
