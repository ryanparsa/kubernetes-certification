#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")
CLUSTER_NAME = "cka-lab-80"

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()

def docker_exec(cmd):
    result = subprocess.run(
        ["docker", "exec", f"{CLUSTER_NAME}-control-plane", "sh", "-c", cmd],
        capture_output=True, text=True,
    )
    return result

class TestClusterInfoExtraction(unittest.TestCase):
    def test_pods_list(self):
        result = docker_exec("cat /opt/course/1/pods.txt")
        self.assertEqual(result.returncode, 0, "pods.txt not found")
        pods = set(filter(None, result.stdout.strip().split('\n')))
        expected_pods = set(kubectl("get", "pods", "-A", "-o", "jsonpath={.items[*].metadata.name}").split())
        self.assertEqual(pods, expected_pods)

    def test_containers_list(self):
        result = docker_exec("cat /opt/course/1/containers.txt")
        self.assertEqual(result.returncode, 0, "containers.txt not found")
        images = result.stdout.strip().split('\n')
        images = [i for i in images if i]
        expected_images = set(kubectl("get", "pods", "-A", "-o", "jsonpath={.items[*].spec.containers[*].image}").split())
        self.assertEqual(set(images), expected_images)
        self.assertEqual(len(images), len(set(images)), "Images are not deduplicated")

    def test_current_context(self):
        result = docker_exec("cat /opt/course/1/context")
        self.assertEqual(result.returncode, 0, "context file not found")
        context = result.stdout.strip()
        # In Kind node, current context should match
        expected_context = docker_exec("kubectl config current-context").stdout.strip()
        self.assertEqual(context, expected_context)

    def test_user_cert(self):
        result = docker_exec("cat /opt/course/1/cert")
        self.assertEqual(result.returncode, 0, "cert file not found")
        cert_content = result.stdout.strip()
        expected_cert_b64 = docker_exec("kubectl config view --raw -o jsonpath='{.users[?(@.name==\"accounts-432\")].user.client-certificate-data}'").stdout.strip()
        # Need to decode it to compare
        import base64
        expected_cert = base64.b64decode(expected_cert_b64).decode('utf-8').strip()
        self.assertEqual(cert_content, expected_cert)

if __name__ == "__main__":
    unittest.main(verbosity=2)
